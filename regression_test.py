import regression_tree
import dtree_build
import sys
import csv


def main(col_names=None):
    # parse command-line arguments to read the name of the input csv file
    # and optional 'draw tree' parameter
    if len(sys.argv) < 2:  # input file name should be specified
        print ("Please specify input csv file name")
        return

    csv_file_name = sys.argv[1]

    data = []
    with open(csv_file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            list = []
            for attribute in row:
                try:
                    list += [float(attribute)]
                except:
                    list += [attribute]
            data.append(list)

    print("Total number of records = ",len(data))
    tree = regression_tree.buildtree(data, min_gain = 0.005, min_samples = 5)

    regression_tree.printtree(tree, '', col_names)

    max_tree_depth = dtree_build.max_depth(tree)
    print("max number of questions=" + str(max_tree_depth))

    if len(sys.argv) > 2: # draw option specified
        import regression_draw
        regression_draw.drawtree(tree, jpeg=csv_file_name+'.jpg')

    if len(sys.argv) > 3:  # create json file for d3.js visualization
        import json
        import dtree_to_json
        json_tree = dtree_to_json.dtree_to_jsontree(tree, col_names)
        print(json_tree)

        # create json data for d3.js interactive visualization
        with open(csv_file_name + ".json", "w") as write_file:
            json.dump(json_tree, write_file)

    print("course ['teaching', 'not minority', 'female', 'english', 50, 30, 'lower', 7, 4] is: ", dtree_build.classify(['teaching', 'not minority', 'female', 'english', 50, 30, 'lower', 7, 4], tree))
    print("course ['teaching', 'not minority', 'male', 'english', 40, 30, 'lower', 6, 4] is: ", dtree_build.classify(['teaching', 'not minority', 'male', 'english', 40, 30, 'lower', 6, 4], tree))
    print("course ['teaching', 'not minority', 'male', 'english', 70, 30, 'lower', 4, 4] is: ", dtree_build.classify(['teaching', 'not minority', 'male', 'english', 70, 30, 'lower', 4, 4], tree))

if __name__ == "__main__":
    col_names = ['rank',
                 'ethnicity',
                 'gender',
                 'language',
                 'age',
                 'class_size',
                 'cls_level',
                 'bty_avg',
                 'prof_eval']
    main(col_names)
