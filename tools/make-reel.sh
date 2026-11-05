#!/bin/bash
# Rebuild img/reel.mp4 and img/reel-poster.jpg: 4.5s of each game, from a Release
# Simulator build of the version on the store. Six 30-second recordings first:
#
#   xcrun simctl launch <udid> com.movusgame.movus -game <id> -sim -sim.landscape \
#       -render.high -coach.off -movus.appearance dark -moverush.onboarded YES \
#       -moverush.seenHowTo "(runner, keeper, swim, slash, squats, boxing)" \
#       -moverush.heroVariant <pin from the app's Tools/shoot-card-art.sh>
#   xcrun simctl io <udid> recordVideo --codec=h264 --force <dir>/<id>.mp4
#
# Then: tools/make-reel.sh <dir> <app repo>
#
# **The crops are not cosmetic.** Under -sim the HUD prints touch instructions
# ("HOLD THE SCREEN TO SQUAT") along the bottom edge, which a camera game must never
# advertise, and Boxing shows a no-camera icon where the tracking panel goes. Keeper,
# Swim, Slash and Squats lose the bottom sixth, and Boxing takes the real panel from
# the App Store screenshot. Look at every cut after re-recording: which moment is
# worth showing depends on the pilot's run.
#
# If the cut points change, change `data-at` in index.html to match.
set -e
R="$1"; B="$2/Tools/AppStore/screenshots/raw/_baked-06-boxing.png"; W=1100; H=506
seg() { ffmpeg -v error -y -ss "$2" -t 4.5 -i "$R/$1.mp4" -vf "transpose=2,crop=iw*${3}:ih*${3}:iw*0.06:0,scale=${W}:${H}:flags=lanczos,fps=30,setsar=1" -an -c:v libx264 -crf 14 -preset veryfast -pix_fmt yuv420p "$R/s-$1.mp4"; }
seg runner 8.5 0.92; seg swim 17 0.84; seg slash 22.5 0.84; seg keeper 19 0.84; seg squats 11.5 0.84
ffmpeg -v error -y -ss 18 -t 4.5 -i "$R/boxing.mp4" -i "$B" -filter_complex "[0:v]transpose=2[v];[1:v]scale=2622:1206,crop=iw*0.115:ih*0.33:iw*0.82:ih*0.11[p];[v][p]overlay=W*0.82:H*0.11,crop=iw*0.92:ih*0.92:iw*0.06:0,scale=${W}:${H}:flags=lanczos,fps=30,setsar=1" -an -c:v libx264 -crf 14 -preset veryfast -pix_fmt yuv420p "$R/s-boxing.mp4"
OUT="$(cd "$(dirname "$0")/../img" && pwd)"
ffmpeg -v error -y -i "$R/s-runner.mp4" -i "$R/s-boxing.mp4" -i "$R/s-swim.mp4" -i "$R/s-slash.mp4" -i "$R/s-keeper.mp4" -i "$R/s-squats.mp4" -filter_complex "[0][1]xfade=fade:duration=0.4:offset=4.1[a];[a][2]xfade=fade:duration=0.4:offset=8.2[b];[b][3]xfade=fade:duration=0.4:offset=12.3[c];[c][4]xfade=fade:duration=0.4:offset=16.4[d];[d][5]xfade=fade:duration=0.4:offset=20.5,format=yuv420p" -an -c:v libx264 -profile:v high -crf 27 -preset slow -movflags +faststart "$OUT/reel.mp4"
ffmpeg -v error -y -ss 2.5 -i "$OUT/reel.mp4" -frames:v 1 -q:v 3 "$OUT/reel-poster.jpg"
