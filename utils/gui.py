from tkinter import Tk, ttk

# Inserting items to the treeview 
# def add_node(treeview: ttk.Treeview, parent_key: str | int, parent_value: dict | str, count: int) -> None:
#     for key, value in parent_value.items():
#         treeview.insert(parent_key, count, count, text=key)
#         count += 1
#         if isinstance(value, dict):
#             count = add_node(treeview, count-1, value, count)
#         else:
#             treeview.insert(count-1, count, count, text=value)
#             count += 1
#     return count

def add_node(treeview: ttk.Treeview, parent: str, node, count: int) -> int:
    """
    Inserts `node` under `parent`.  `node` may be a dict, a list, or a primitive.
    Returns the updated count.
    """
    # --- DICTIONARY: recurse on its items ---
    if isinstance(node, dict):
        for key, value in node.items():
            # insert the dict key
            treeview.insert(parent, 'end', iid=str(count), text=str(key))
            count += 1
            # recurse into the value
            count = add_node(treeview, str(count - 1), value, count)

    # --- LIST: recurse on each element ---
    elif isinstance(node, list):
        # optional: label the list node itself
        list_iid = str(count)
        treeview.insert(parent, 'end', iid=list_iid, text=f"[list, {len(node)} items]")
        count += 1

        for idx, item in enumerate(node):
            # give each item a sub‑label "[0]", "[1]", etc.
            item_iid = str(count)
            treeview.insert(list_iid, 'end', iid=item_iid, text=f"[{idx}]")
            count += 1
            # recurse into the item
            count = add_node(treeview, item_iid, item, count)

    # --- LEAF: just insert the value as a string ---
    else:
        treeview.insert(parent, 'end', iid=str(count), text=str(node))
        count += 1

    return count

def create_gui(hierarchy: dict) -> None:
    app = Tk()  
    app.title("GUI Visualization of nested dictionaries") 

    ttk.Label(app, text ="Treeview(hierarchical)").pack()

    frame = ttk.Frame(app)
    frame.pack(expand=True, fill='both')

    treeview = ttk.Treeview(frame)
    treeview.pack(side='left', expand=True, fill='both')  

    v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
    v_scrollbar.pack(side='right', fill='y')

    h_scrollbar = ttk.Scrollbar(app, orient="horizontal", command=treeview.xview)
    h_scrollbar.pack(side='bottom', fill='x')

    treeview.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    count = 0
    for key, value in hierarchy.items():
        treeview.insert("", count, count, text=key)
        count += 1
        if isinstance(value, dict):
            count = add_node(treeview, count-1, value, count) # count needs to be returned to keep the count updated
        else:
            treeview.insert(count-1, count, count, text=value)
            count += 1

    treeview.pack(expand=True, fill='both')
    app.mainloop()