#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)
import os
import hw3
import argparse

parser = argparse.ArgumentParser(
    description="Part of speech tagging.")
parser.add_argument("-d", "--data", default="data",
                    help="The base path for the data files.")
parser.add_argument("-o", "--outfile", default="output.txt",
                    help="The file where the output should be written.")
parser.add_argument("--estimate", action="store_true",
                    help="Estimate the interpolation coefficients from "
                    "the training data?")
parser.add_argument("--lambda2", default=0.3, type=float,
                    help="The bigram weight.")
parser.add_argument("--lambda3", default=0.6, type=float,
                    help="The trigram weight.")


if __name__ == "__main__":
    args = parser.parse_args()
    data_path = args.data

    # Load all the datasets.
    print("Loading training data")
    training_data = hw3.read_dataset(os.path.join(data_path,
                                                  "en-wsj-train.pos"))

    print("Loading in-domain validation data")
    dev_in_data = hw3.read_dataset(os.path.join(data_path, "en-wsj-dev.pos"))

    print("Loading out-of-domain validation data")
    dev_out_data = hw3.read_dataset(os.path.join(data_path,
                                                 "en-web-weblogs-dev.pos"))

    print("Loading out-of-domain test data")
    test_data = hw3.read_dataset(os.path.join(data_path, "en-web-test.blind"))

    # Set up and train the local tag scorer.
    print("Training scorer")
    scorer = hw3.TrigramScorer(lambda2=args.lambda2, lambda3=args.lambda3)
    scorer.train(training_data)
    if args.estimate:
        print("Estimating interpolation coefficients")
        scorer.estimate_lambdas()

    model = hw3.POSTagger(scorer)

    print("Testing in-domain performance")
    acc, unk = model.test(dev_in_data)
    print("Accuracy: {0:.4f}, Unknown: {1:.4f}".format(acc*100, unk*100))

    print("Testing out-of-domain performance")
    acc, unk = model.test(dev_out_data)
    print("Accuracy: {0:.4f}, Unknown: {1:.4f}".format(acc*100, unk*100))

    print("Writing out-of-domain predictions")
    model.test(test_data, outfile=args.outfile)
