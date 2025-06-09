VENV_PATH="./rufa-venv"

MAIN_PY_PATH="./main.py"

SCREEN_NAME="RuFA-Hub"

screen -dmS $SCREEN_NAME bash -c "
  source $VENV_PATH/bin/activate;
  python3 $MAIN_PY_PATH;
  exec bash"
