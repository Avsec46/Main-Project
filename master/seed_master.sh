# !/bin/bash
fixtures=$(ls ./master/seed/)
while IFS= read -r fixture; do
    echo -n "Seeding "
    echo $fixture
    py manage.py loaddata ./master/seed/$fixture
done <<< "$fixtures"