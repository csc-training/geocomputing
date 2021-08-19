origin_x=379190
origin_y=6673340
piece_size=400
for x in 0 1
do
    for y in 0 1
    do
        bb=($[$origin_x+$piece_size*$x] $[$origin_x+$piece_size*($x+1)] $[$origin_y+$piece_size*$y] $[$origin_y+$piece_size*($y+1)])
        echo pdal pipeline crop_pipeline.json --filters.crop.bounds="([${bb[0]},${bb[1]]}],[${bb[2]},${bb[3]}])" --writers.las.filename=data/part_$x$y.laz
        pdal pipeline crop_pipeline.json --filters.crop.bounds="([${bb[0]},${bb[1]]}],[${bb[2]},${bb[3]}])" --writers.las.filename=data/part_$x$y.laz

    done
done


