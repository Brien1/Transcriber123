echo '#!/bin/sh'>/app/.apt/usr/bin/lilypond
echo 'export LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu/lilypond/2.20.0/guile"'>>/app/.apt/usr/bin/lilypond
echo 'exec "/app/.apt/usr/bin/lilypond.real" "$@"'>>/app/.apt/usr/bin/lilypond
