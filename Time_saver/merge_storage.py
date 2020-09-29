from login import login

import time
from lxml.html import fromstring

def merge(server, ids, session=""):
    """
    Merge specific EQ IDs / all EQs in storage (good for non-premium players).
    
    For all eqs under specific Q, write that Q.
    Specific ids: separated them by a comma.
    
    Examples:
    merge("alpha", "Q6") -> Merge all Q1-6 eqs in your storage.
    merge("alpha", "10, 15, 18") -> Merge eqs id 10, 15 and 18
    """    
    URL = f"https://{server}.e-sim.org/"
    if not session:
        session = login(server)

    if "," in ids:
        EQ1, EQ2, EQ3 = [eq.strip() for eq in ids.split(",")]
        payload = {'action': "MERGE", f'itemId[{EQ1}]': EQ1, f'itemId[{EQ2}]': EQ2, f'itemId[{EQ3}]': EQ3}
        merge_request = session.post(URL + "equipmentAction.html", data=payload)
        print(merge_request.url)

    else:
        max_q_to_merge = int(ids.lower().replace("q", ""))  # max_q_to_merge - including
        for _ in range(5):
            get_eqs = session.get(f'{URL}storage.html?storageType=EQUIPMENT')
            tree = fromstring(get_eqs.content)
            IDs = tree.xpath(f'//*[starts-with(@id, "cell")]/a/text()')
            items = tree.xpath(f'//*[starts-with(@id, "cell")]/b/text()')
            DICT = {}
            for ID, item in zip(IDs, items):
                Q = int(item.split()[0].replace("Q", ""))
                if Q < max_q_to_merge + 1:
                    if Q not in DICT:
                        DICT[Q] = []
                    DICT[Q].append(int(ID.replace("#", "")))
            for i in range(1, max_q_to_merge + 1):
                if i in DICT and len(DICT[i]) > 2:
                    for z in range(int(len(DICT[i]) / 3)):
                        EQ1, EQ2, EQ3 = DICT[i][z*3:z*3 + 3]
                        payload = {'action': "MERGE", f'itemId[{EQ1}]': EQ1, f'itemId[{EQ2}]': EQ2,
                                   f'itemId[{EQ3}]': EQ3}
                        merge_request = session.post(URL + "equipmentAction.html", data=payload)
                        print(merge_request.url)
                        time.sleep(1)
                        if str(merge_request.url) == "http://www.google.com/":
                            # e-sim error
                            time.sleep(5)

                        elif "?actionStatus=CONVERT_ITEM_OK" not in str(merge_request.url):
                            # no money etc
                            break
    return session


if __name__ == "__main__":
    print(merge.__doc__)
    server = input("Server: ")
    ids = input("EQs ids, or max Q to merge: ")
    merge(server, ids)
    input("Press any key to continue")
