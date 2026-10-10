"""Read the native save's anonymous selection objects; no game or file mutation."""
import audit_save as q
def selected_history(raw):
    text=q.block(q.block(raw,'open_player_event_selection_history'),'selected')
    result=[];depth=0;start=None
    for token,before,after in q.tokens(text):
        if token=='{':
            if depth==0:start=after
            depth+=1
        elif token=='}':
            assert depth>0,'Unexpected closing brace in native history'
            depth-=1
            if depth==0:
                entry=q.scalars(text[start:before])
                assert set(entry)=={'player_event','human','option'},'Unknown native selection fields'
                result.append(entry)
        elif depth==0:raise ValueError('Expected anonymous native history object')
    assert depth==0,'Unclosed native selection object'
    return result
