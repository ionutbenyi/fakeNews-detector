
class StatisticsInterpreter:

    def interpret_results(self, true_positive, false_positive, true_negative, false_negative):
        # confusion matrix:
        # compute precision & recall
        if (true_positive + false_positive) != 0:
            precision = true_positive / (true_positive + false_positive)
            print("Precision = "+ str(precision))

        if (true_negative + false_negative) != 0:
            neg_precision = true_negative/(true_negative + false_negative)
            print("Negative precission = " + str(neg_precision))

        if (true_positive + false_negative) != 0:
            recall = true_positive / (true_positive + false_negative)
            print("Recall = "+str(recall))
        