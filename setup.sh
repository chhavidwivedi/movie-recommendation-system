mkdir -p ~/.streamlit/

echo"\
[server]
port=\$PORT\n\
enableCORS=false
headless=true
">~/.streamlit/config.toml