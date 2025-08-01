src="/mnt/big/music/Game Soundtracks/Animal Crossing/401 - New Horizons"
dst="clear"
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

dst="rainy"
for hour in $(seq 0 11); do
    padded=$(printf "%02d" $hour)
    if [ "$padded" = "00" ]; then
        ln -sv "$src"/*\ -\ 12\ AM\ \(Midnight\)\ -\ Rainy.flac $dst/"$padded.flac"
    else
        ln -sv "$src"/*\ -\ $hour\ AM\ -\ Rainy.flac $dst/"$padded.flac"
    fi
done

for hour in $(seq 12 23); do
    pmhour=$((hour-12))
    padded=$(printf "%02d" $hour)
    if [ "$padded" = "12" ]; then
        ln -sv "$src"/*\ -\ 12\ PM\ \(Noon\)\ -\ Rainy.flac $dst/"$padded.flac"
    else
        ln -sv "$src"/*\ -\ $pmhour\ PM\ -\ Rainy.flac $dst/"$padded.flac"
    fi
done

dst="snowy"
for hour in $(seq 0 11); do
    padded=$(printf "%02d" $hour)
    if [ "$padded" = "00" ]; then
        ln -sv "$src"/*\ -\ 12\ AM\ \(Midnight\)\ -\ Snowy.flac $dst/"$padded.flac"
    else
        ln -sv "$src"/*\ -\ $hour\ AM\ -\ Snowy.flac $dst/"$padded.flac"
    fi
done

for hour in $(seq 12 23); do
    pmhour=$((hour-12))
    padded=$(printf "%02d" $hour)
    if [ "$padded" = "12" ]; then
        ln -sv "$src"/*\ -\ 12\ PM\ \(Noon\)\ -\ Snowy.flac $dst/"$padded.flac"
    else
        ln -sv "$src"/*\ -\ $pmhour\ PM\ -\ Snowy.flac $dst/"$padded.flac"
    fi
done

