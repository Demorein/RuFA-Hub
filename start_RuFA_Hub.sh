VENV_PATH="ROUTE TO VENV"

MAIN_PY_PATH="ROUTE TO MAIN.PY"

SCREEN_NAME="RuFA-Hub"

screen -dmS $SCREEN_NAME bash -c "
  source $VENV_PATH/bin/activate;
  python3 $MAIN_PY_PATH;
  exec bash"
