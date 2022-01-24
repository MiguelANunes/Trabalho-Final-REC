INPUTS="./Inputs"
for i in $(seq 0 119); do
    "$INPUTS"/"clean"
    "$INPUTS"/"netem$i"
    python3 network_test.py < "$INPUTS"/"teste$i"
    "$INPUTS"/"clean"
done