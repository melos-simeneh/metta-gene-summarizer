; Import required namespaces
; !(import! &summary data:gene_with_summary)
!(import! &self data:gene)
!(import! &self utils)

; ------------------------------------------------------------------------------
; Function: extract_gene_data
; Purpose: Extract structured gene data from raw gene facts
; ------------------------------------------------------------------------------
(= (extract_gene_data) 
    (match &self
        (,  
            (gene $gene_id)  
            (gene_type (gene $gene_id) $gene_type)  
            (chr (gene $gene_id) $chromosome)  
            (start (gene $gene_id) $start_pos)  
            (end (gene $gene_id) $end_pos)  
            (gene_name (gene $gene_id) $gene_name)  
            (synonyms (gene $gene_id) $synonyms)  
        )
        ($gene_id $gene_type $chromosome $start_pos $end_pos $gene_name $synonyms)
    )
)


!(bind! &summary (new-space))

; ------------------------------------------------------------------------------
; Data Processing Pipeline:
; 1. Extract raw gene info in the knowledge space &self.
; 2. Summarize it using Gemini
; 3. Write the summarized output to a file
; ------------------------------------------------------------------------------
; !(let* 
;   (
;    ($raw_data (extract_gene_data))
;    ($summarized_data (summarize_gene_data $raw_data))
;    ($result (write_summary $summarized_data gene_with_summary.metta))
;   )
;   ($result)
; )




!(let* 
  (
   ($raw_data (extract_gene_data))
   ($summarized_data (summarize_gene_data $raw_data))
   ($result (write_summary $summarized_data gene_with_summary.metta))
   ($space_k (format_new_gene_data $summarized_data))
   ($space (add-atom &summary $space_k))
  )
  ($result)
)
; ------------------------------------------------------------------------------
; Function: gene_data_with_summary
; Purpose: Match full gene data, including the summary, from enriched facts
;          in the knowledge space &summary.
; ------------------------------------------------------------------------------
(= (gene_data_with_summary) 
    (match &summary
        (,
            (gene $gene_id)
            (gene_type (gene $gene_id) $gene_type)
            (chr (gene $gene_id) $chromosome)
            (start (gene $gene_id) $start_pos)
            (end (gene $gene_id) $end_pos)
            (gene_name (gene $gene_id) $gene_name)
            (synonyms (gene $gene_id) $synonyms)
            (summary (gene $gene_id) $summary)
        )
        ($gene_id $gene_type $chromosome $start_pos $end_pos $gene_name $synonyms $summary)
    )
)

; !(gene_data_with_summary)
; ------------------------------------------------------------------------------
; Save full summary to a human-readable text file
; ------------------------------------------------------------------------------
!(let $data (gene_data_with_summary) (save_human_readable_output $data gene_summary_result.txt))
