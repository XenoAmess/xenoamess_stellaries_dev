"""Adversarial liveness cases: local empty lists must not hide live global state."""
import unittest

from check_settlement_liveness_1020 import inspect_liveness


JOB = "type=replicator workforce=112 automated_workforce=0 planet=18 pop_groups={ { pop_group=90 amount=112 } }"


def snapshot(*, alive=False, extra_group="", owner_refs="", job=JOB, extra_job="", job_ids="7"):
    planet = "planet_class=pc_machine colony=18 owner=0 controller=0" if alive else "planet_class=pc_shattered colony=18"
    groups = "90={ planet=18 size=112 }" if alive else "90=none"
    colony = "pop_groups={90} num_sapient_pops=112 employable_pops=112" if alive else "pop_groups={}"
    return ("planets={ planet={ 1={" + planet + "} } } "
            "colony={ 18={" + colony + " pop_jobs={" + job_ids + "} } } "
            "country={ 0={" + owner_refs + "} } "
            "pop_groups={" + groups + " " + extra_group + "} "
            "pop_jobs={ 7={" + job + "} " + extra_job + "}")


class LivenessTests(unittest.TestCase):
    def setUp(self):
        self.before = snapshot(alive=True)

    def verify(self, after):
        return inspect_liveness(self.before, after, 1)

    def test_dead_allocation_cache_allowed_but_before_rejected(self):
        self.assertEqual(self.verify(snapshot())["status"], "PASS_SCOPED")
        self.assertEqual(self.verify(self.before)["status"], "FAIL")

    def test_unlisted_global_population_is_not_hidden(self):
        result = self.verify(snapshot(extra_group="91={planet=18 size=1}"))
        self.assertFalse(result["checks"]["no_global_population_at_source_colony"])
        self.assertEqual(result["status"], "FAIL")

    def test_live_allocation_even_on_another_colony_is_rejected(self):
        result = self.verify(snapshot(extra_group="90={planet=0 size=112}"))
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["jobs"]["7"]["all_population_references_dead"])

    def test_country_reference_is_rejected(self):
        for field, identity in (("owned_planets", 18), ("controlled_colonies", 18), ("controlled_planets", 1)):
            with self.subTest(field=field):
                self.assertEqual(self.verify(snapshot(owner_refs=f"{field}={{{identity}}}"))["status"], "FAIL")

    def test_modified_job_and_automatic_production_are_rejected(self):
        for job in (JOB.replace("workforce=112", "workforce=113"),
                    JOB.replace("automated_workforce=0", "automated_workforce=1")):
            with self.subTest(job=job):
                self.assertEqual(self.verify(snapshot(job=job))["status"], "FAIL")

    def test_unchanged_automatic_production_is_also_rejected(self):
        job = JOB.replace("automated_workforce=0", "automated_workforce=1")
        before = snapshot(alive=True, job=job)
        self.assertEqual(inspect_liveness(before, snapshot(job=job), 1)["status"], "FAIL")

    def test_new_global_job_cannot_hide_outside_colony_list(self):
        extra = "8={type=replicator workforce=1 automated_workforce=0 planet=18}"
        self.assertEqual(self.verify(snapshot(extra_job=extra))["status"], "FAIL")

    def test_new_or_missing_listed_job_is_rejected(self):
        self.assertEqual(self.verify(snapshot(job_ids="7 8"))["status"], "FAIL")

    def test_fully_removed_jobs_are_allowed(self):
        after = snapshot(job_ids="").replace("pop_jobs={ 7={" + JOB + "} }", "pop_jobs={}")
        self.assertEqual(self.verify(after)["status"], "PASS_SCOPED")

    def test_removed_colony_reference_is_allowed_but_replacement_is_not(self):
        after = snapshot()
        self.assertEqual(self.verify(after.replace("pc_shattered colony=18", "pc_shattered"))["status"], "PASS_SCOPED")
        self.assertEqual(self.verify(after.replace("pc_shattered colony=18", "pc_shattered colony=19"))["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
