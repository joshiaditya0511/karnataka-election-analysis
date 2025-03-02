# Karnataka Assembly Elections: Data Analysis

This project provides a comprehensive analysis of the Karnataka Assembly Elections. Through various insights and visualizations, it examines multiple facets of the elections using data from multiple sources. Explore the findings directly on the [website](https://kea.adityajoshi.in).

## Contents
- [Links](#links)
- [Project Overview](#project-overview)
- [Tools and Tech Used](#tools-and-tech-used)
- [Sources and References](#sources-and-references)
- [Change Log](#change-log)

## Links

- [Project Website](https://kea.adityajoshi.in)
- [LinkedIn](https://www.linkedin.com/in/joshiaditya0511)
- [Personal Website](https://adityajoshi.in)

## Project Overview

This analysis dives deep into the Karnataka Assembly Elections, exploring elements such as vote counts, candidate details, vote margins, and the impact of events like the Bharat Jodo Yatra. All visualizations are interactive to provide an engaging and informative user experience.

## Tools and Tech Used

### Data Gathering:

- **Web Scraping**:
  - `Requests`: Sent GET requests to retrieve webpage content.
  - `BeautifulSoup`: Parsed HTML for relevant data extraction.
  - `Selenium`: Interacted with dynamic pages, ensuring smoother data fetching.
  - `asyncio`: Enhanced performance with asynchronous requests for efficient data retrieval.

- **PDF Extraction**:
  - Processed over 57,000 PDFs to extract voter data for the 2023 elections.
  - `PyPDF2`: Processed PDFs, retaining only essential pages.
  - `pdf2image`: Converted PDF pages to images.
  - `OpenCV`: Detected table borders for precise data extraction.
  - `TesseractOCR`: Extracted text data within table areas.
  - `asyncio` and `multiprocessing`: Enabled asynchronous downloads and parallel processing of PDFs.

### Data Wrangling:

- `Pandas` and `Regular Expressions`: Key tools for data cleaning and organization.
- `OpenAI API`: Used OpenAI Batch API with GPT-4o-mini for segmenting and categorizing education and profession data from candidate details.

### Data Visualization:

- `Plotly`: Main library for crafting interactive visualizations.
- `Flourish Studio`: Created and embedded the Parliamentary Chart as an HTML component.

### Website and Deployment:

- **Frontend**: Built using `HTML`, `Bootstrap`, and `JavaScript` to create a **static** and **responsive** site.
- **Hosting**: Deployed on an `AWS EC2` instance using the free tier, with `NGINX` configured as the web server for efficient delivery.

### Miscellaneous:

- `MapShaper`: Converted Karnataka's assembly boundaries shapefile to GeoJSON and optimized boundaries for faster rendering.

## Sources and References

- **[MyNeta](https://www.myneta.info/)**: Data on candidate assets, liabilities, criminal cases, profession, and education.
- **[NDTV](https://www.ndtv.com/)**: Vote counts for all candidates in the 2023 elections.
- **[OpenCity](https://opencity.in/)**: Detailed results from the 2013 Assembly elections.
- **[ECI (Election Commission of India)](https://eci.gov.in/)**: Detailed results from the 2018 elections.
- **[CEO (Chief Election Officer) of Karnataka](https://ceo.karnataka.gov.in/en)**: Gender distribution data on eligible voters, provided in PDFs.
- **[KGIS (Karnataka Geographic Information System)](https://kgis.ksrsac.in/kgis/)**: Shapefile for assembly constituency boundaries.
- **[MapShaper](https://mapshaper.org/)**: Shapefile conversion to GeoJSON, smoothing boundaries for visualization.
- **[OpenAI](https://openai.com/)**: Used for segmenting and classifying candidate details on education and profession.

## Change Log

- **Transition to a Static Site**: The project originally utilized a dynamic backend with a MySQL database and Streamlit for visualizations. However, due to the stationary nature of the data (i.e., it will not change over time), the database backend was removed. This allowed the project to move to a static site, reducing backend load and enhancing performance.
- **Deployment Update**: The Streamlit-hosted site was replaced with a static site built with HTML, Bootstrap, and JavaScript, hosted on a free-tier AWS EC2 instance using NGINX. This change improves site speed and responsiveness while providing a smoother user experience.
