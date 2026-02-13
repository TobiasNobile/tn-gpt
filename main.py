import sys
import streamlit.web.cli as stcli

def main():
    sys.argv = ["streamlit", "run", "app/chat.py", "--server.port=8501"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()