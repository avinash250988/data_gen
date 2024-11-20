   mkdir -p ~/.streamlit/

   echo "\
   [server]\n\
   headless = true\n\
   enableCORS=false\n\
   port = 8000\n\
   address = '0.0.0.0'\n\
   " > ~/.streamlit/config.toml
