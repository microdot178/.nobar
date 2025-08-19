#!/bin/bash

# .nobar installation script

set -e

CONFIG_DIR="$HOME/.config/nobar"
BIN_DIR="$HOME/.local/bin"
VENV_DIR="$HOME/.virtualenvs/nobar"
CURRENT_DIR=$PWD

mkdir -p "$CONFIG_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$VENV_DIR"

echo "Creating default config..."
cat >"$CONFIG_DIR/config.toml" <<'EOF'
[workspaces]
height = 40
color = 'gray'
focused = 'white'
background = 'black'
position = [0, 0]
fade_out = 5000

[info]
height = 40
color = 'white'
background = 'black'
position = ['right', 0]
fade_out_on_hover = true
EOF

echo "Creating executable wrapper..."
cat >"$BIN_DIR/nobar" <<EOF
#!/bin/bash
source $VENV_DIR/bin/activate
python $CURRENT_DIR/main.py $CONFIG_DIR/config.toml
EOF

chmod +x "$BIN_DIR/nobar"

echo "Installing Python dependencies..."
python -m venv $VENV_DIR
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt
