!(import! &self data:gene)

; This matches gene-related facts and extracts structured information about each gene.
(= (extract_gene_data) 
    (match &self
        (,  ; Match a pattern with the following structure:
            (gene $gene_id)  
            (gene_type (gene $gene_id) $gene_type)  
            (chr (gene $gene_id) $chromosome)  
            (start (gene $gene_id) $start_pos)  
            (end (gene $gene_id) $end_pos)  
            (gene_name (gene $gene_id) $gene_name)  
            (synonyms (gene $gene_id) $synonyms)  
        )
        ; Return these as a tuple
        ($gene_id $gene_type $chromosome $start_pos $end_pos $gene_name $synonyms)
    )
)

; Execute the extraction function to retrieve structured gene information
!(extract_gene_data)
