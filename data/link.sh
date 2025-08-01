src="/mnt/big/music/Game Soundtracks/Animal Crossing/401 - New Horizons"
dst="raw"
for hour in $(seq 0 11); do
    padded=$(printf "%02d" $hour)
    if [ "$padded" = "00" ]; then
        ln -sv "$src"/*\ -\ 12\ AM\ \(Midnight\).flac $dst/"$padded.flac"
    else
        ln -sv "$src"/*\ -\ $hour\ AM.flac $dst/"$padded.flac"
    fi
done

for hour in $(seq 12 23); do
    pmhour=$((hour-12))
    padded=$(printf "%02d" $hour)
    if [ "$padded" = "12" ]; then
        ln -sv "$src"/*\ -\ 12\ PM\ \(Noon\).flac $dst/"$padded.flac"
    else
        ln -sv "$src"/*\ -\ $pmhour\ PM.flac $dst/"$padded.flac"
    fi
done
