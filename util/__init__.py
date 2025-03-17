from typing import List, Any, Iterator


def requireAll(entityLists: List[Iterator[Any]]) -> Iterator[Any]:
    entityLists = [list(l) for l in entityLists]
    entities = [entity for entityList in entityLists for entity in entityList]
    filteredEntities = []

    for entity in entities:
        satisfiesAll = True
        for entityList in entityLists:
            if entity not in entityList:
                satisfiesAll = False
                break
        if satisfiesAll:
            filteredEntities.append(entity)

    return filteredEntities
