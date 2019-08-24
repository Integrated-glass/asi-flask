import math as m

def paginate(firstPage, currentPage, lastPage, radius, urlGenerator):
  # TODO: precondition & documentation
  result = {}
  pagesResult = []

  pagesResult.append((firstPage, urlGenerator(firstPage)))
  if (firstPage + radius + 1 < currentPage):
    pagesResult.append((-1, urlGenerator(-1)))

  for i in range(max([currentPage - radius, firstPage + 1]), min([currentPage + radius + 1, lastPage + 1])):
    pagesResult.append((i, urlGenerator(i)))

  if (currentPage + radius + 1 <= lastPage):
    if (currentPage + radius + 1 < lastPage):
      pagesResult.append((-1, urlGenerator(-1)))
    pagesResult.append((lastPage, urlGenerator(lastPage)))

  result["pages"] = pagesResult

  previousPage = currentPage - 1
  if previousPage >= firstPage:
    result["previousPage"] = (previousPage, urlGenerator(previousPage))

  nextPage = currentPage + 1
  if nextPage <= lastPage:
    result["nextPage"] = (nextPage, urlGenerator(nextPage))

  return result

def currentPageNumber(startIndex, itemsPerPage):
  return (startIndex // itemsPerPage) + 1

def lastPageNumber(totalPages, itemsPerPage):
  return m.ceil(totalPages / itemsPerPage)

def getOffsetForPage(page, itemsPerPage):
  return (page - 1) * itemsPerPage
