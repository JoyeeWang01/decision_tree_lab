import dtree_build

def average_prediction(leaf_labels):
#    total = 0
#   sum = 0
#    for value in leaf_labels:
#        total += 1
#        sum += float(value)
#    return round(float(sum/total),2)
    total = 0
    result = 0
    for label, count in leaf_labels.items():
        total += count
        result += count*float(label)
    return round(float(result/total), 2)

def average(rows):
#    results = []
#    for row in rows:
#        # The result is the last column
#        r = row[len(row) - 1]
#        results += [r]
#    return results
    results = {}
    for row in rows:
        # The result is the last column
        r = row[len(row) - 1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results

def buildtree(rows, scoref=dtree_build.variance,
              min_gain=0, min_samples=0):
    if len(rows) == 0:
        return dtree_build.decisionnode()
    current_score = scoref(rows)

    # Set up accumulator variables to track the best criteria
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1
    for col in range(0, column_count):
        # Generate the list of different values in
        # this column
        column_values = {}
        for row in rows:
            column_values[row[col]] = 1
        # Now try dividing the rows up for each value
        # in this column
        for value in column_values.keys():
            (set1, set2) = dtree_build.divideset(rows, col, value)

            # Information gain
            p = float(len(set1)) / len(rows)
            gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)
            if gain > best_gain and len(set1) > min_samples and len(set2) > min_samples and gain > min_gain:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    # Create the sub branches
    if best_gain > 0:
        trueBranch = buildtree(best_sets[0], scoref, min_gain, min_samples)
        falseBranch = buildtree(best_sets[1], scoref, min_gain, min_samples)
        return dtree_build.decisionnode(col=best_criteria[0], value=best_criteria[1],
                            tb=trueBranch, fb=falseBranch)
    else:
        return dtree_build.decisionnode(results=average(rows))

def printtree(tree, current_branch, attributes=None,  indent='', leaff=average_prediction):
    # Is this a leaf node?
    if tree.results != None:
        print(indent + current_branch + str(leaff(tree.results)))
    else:
        # Print the split question
        split_col = str(tree.col)
        if attributes is not None:
            split_col = attributes[tree.col]
        split_val = str(tree.value)
        if type(tree.value) == int or type(tree.value) == float:
            split_val = ">=" + str(tree.value)
        print(indent + current_branch + split_col + ': ' + split_val + '? ')

        # Print the branches
        indent = indent + '  '
        printtree(tree.tb, 'T->', attributes, indent)
        printtree(tree.fb, 'F->', attributes, indent)
