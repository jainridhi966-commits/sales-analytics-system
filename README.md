# Sales Analytics System

## Overview
This project is a Python-based Sales Data Analytics System that:
- Reads and cleans sales transaction data
- Validates and filters transactions
- Performs sales analysis (revenue, regions, products, customers, trends)
- Integrates with an external API to enrich product data
- Generates a comprehensive sales report in text format

The project is structured as part of a graded assignment and demonstrates:
- File handling
- Data processing
- API integration
- Report generation



## Project Structure

sales-analytics-system/
│
├── main.py                      
├── report_generator.py          
├── README.md                    
│
├── utils/
│   ├── file_handler.py          
│   ├── data_processor.py        
│   └── api_handler.py           
│
├── data/
│   └── sales_data.txt            
│
├── output/
│   └── sales_report.txt          
│
└── requirements.txt              
