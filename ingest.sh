
echo "Activating environment"
source .env/bin/activate

echo "Running company_ingestor"
python -m src.Ingestor.company_ingestor


echo "Running psc_ingestor"

python -m src.Ingestor.psc_ingestor

echo "DONE"
