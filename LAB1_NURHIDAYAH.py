import streamlit as st
import requests
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# Function to retrieve protein sequence data based on the given Uniprot ID
def retrieve_data(protein_id):
    url = f"https://www.uniprot.org/uniprot/{protein_id}.fasta"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Extracting the sequence from the response
        fasta_data = response.text.splitlines()
        protein_sequence = ''.join(fasta_data[1:])  # Join all lines except the header
        return protein_sequence
    else:
        st.error(f"Failed to retrieve data for ID: {protein_id}. Please check the ID and try again.")
        return None

# Function to perform basic analysis on the protein sequence
def get_basic_analysis(sequence):
    analysis = ProteinAnalysis(sequence)
    length = len(sequence)
    aa_composition = analysis.get_amino_acids_percent()
    molecular_weight = analysis.molecular_weight()
    isoelectric_point = analysis.isoelectric_point()
    
    return {
        "Length": length,
        "Amino Acid Composition": aa_composition,
        "Molecular Weight": molecular_weight,
        "Isoelectric Point": isoelectric_point
    }

# Streamlit app interface
st.title('Lab 1 - Nur Hidayah')

protein_id = st.text_input('Enter Uniprot ID')
retrieve = st.button('Retrieve')

if retrieve:
    if protein_id != "":
        # Retrieve the protein sequence data
        protein_sequence = retrieve_data(protein_id)
        
        if protein_sequence:
            st.subheader('Protein Sequence')
            st.text(protein_sequence)
            
            # Get basic analysis of the protein sequence
            analysis_result = get_basic_analysis(protein_sequence)
            
            st.subheader('Basic Analysis Results')
            for key, value in analysis_result.items():
                st.write(f"{key}: {value}")
    else:
        st.warning('Please enter Uniprot ID')
