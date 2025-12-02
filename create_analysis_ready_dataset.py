import argparse
import pandas as pd
import os

parser = argparse.ArgumentParser()

# Setup Argument Parser for OmniBenchmark

parser = argparse.ArgumentParser(description="Get real cancer proteomics data")

parser.add_argument("-i", "--input", required = True, help="Input dataset to be manipulated")
parser.add_argument("--output_dir", type=str, required=True,
                        help="Output directory")
parser.add_argument("--name", type=str, required=True,
                        help="Dataset name")

parser.parse_args()


def main():

    args = parser.parse_args()
    input_data_path = args.input

    input_dataframe = pd.read_csv(input_data_path).loc[:, ~pd.read_csv(input_data_path).columns.str.contains('^Unnamed')]
    names_ensembl_ids = input_dataframe[["Name","Database_ID"]]
    input_dataframe.set_index('Name', inplace=True)
    
    # ready to use expression matrix
    expression_matrix = input_dataframe.drop(["Database_ID"], axis = 1)

    # labels with name to be mapped for analysis
    sample_ids = expression_matrix.columns#colnames(expression_m_samples_only)[2:length(colnames(expression_m_samples_only))]
    labels_dict = {}
    for id in sample_ids:
        if "N" in id:
            labels_dict[id] = "N"
        else:
            labels_dict[id] = "T"
    
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Construct output file paths
    output_file = os.path.join(args.output_dir, f"{args.name}.dataset.csv")
    sample_labels_file = os.path.join(args.output_dir, f"{args.name}.sample_labels.csv")
    
    expression_matrix.to_csv(output_file, index = True)
    sample_labels_df = pd.DataFrame(list(labels_dict.items()), columns=["Sample ID", "Group Label"])
    sample_labels_df.to_csv(sample_labels_file, index=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, exit with a non-zero code
        import sys
        sys.exit(1)

