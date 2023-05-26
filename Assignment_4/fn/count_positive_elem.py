def count_positive_elem(arr, dim):
  count = 0
  for i in range(dim):
    if arr[i] < 1: continue
    count += 1
  return count