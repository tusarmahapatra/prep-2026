import heapq
def minimizeReleaseDays(schedule, refactorDays):
    # is there a release on i [(i+1)th day]? if yes, which module [c]
    # check if the refactoring of c is done, if yes, release
    # else, refactor it and reduce the value from the refactorDays array
    # prioritize earliest schedules
    releasePriority = {}
    for i, c in enumerate(schedule):
        if c > 0:
            if c in releasePriority:
                return -1
            releasePriority[c] = i
    if len(releasePriority)!=len(refactorDays):
        return -1
    
    modules = []
    for module in range(1, len(refactorDays)+1):
        modules.append((releasePriority[module], module))

    modules.sort()
    heap = []
    currentDay = 0
    index = 0
    released = set()
    while currentDay<len(schedule) or heap:
        while index<len(refactorDays) and modules[index][0]>=currentDay:
            rlsP, mod = modules[index]
            heapq.heappush(heap, (rlsP, refactorDays[mod-1], mod))
            index+=1
        if currentDay<len(schedule) and schedule[currentDay]>0:
            mod = schedule[currentDay]
            if mod not in released:
                for rlsP, ref, m in heap:
                    if m==mod:
                        return -1
                released.add(mod)

        else:
            if heap:
                rlsP, ref, mod = heapq.heappop(heap)
                ref-=1
                if ref>0:
                    if currentDay+1> rlsP:
                        return -1
                    
                    heapq.heappush(heap, (rlsP, ref, mod))

        currentDay+=1

    return max(releasePriority.values())+ 1
        
        

        

schedule = [1, 0, 0, 1, 2, 2, 1, 2]
refactorDays = [1, 2]
print(minimizeReleaseDays(schedule, refactorDays))