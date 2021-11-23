## Compatibility

##### Built and tested under

- Python 3.8.5
- pip 20.0.2

## Adding virtual environments

- run this command in base project directory

```
python -m venv venv
```

- then activate

linux/MacOS `source venv/bin/activate`

windows(CMD) `venv\Scripts\activate`

[Python env Docs](docs.python.org/3/library/venv.html)

## Installing packages

```bash
pip install -r requirements.txt 
```

## Create conditions for application run

- in terminal at project folder for development
####For development config
```bash
export BOT_ENV=development
```
####For Ethereum Chain config
```bash
export BOT_ENV=eth
```
####For Binance Smart Chain config
```bash
export BOT_ENV=bsc
```
## Run application
```bash
python3 prices.py 
```

- Output 
```
coin_pair|swap_pair|date_added|price_defference|dex_1|dex_2|dex_3|dex_4|dex_5|dex_6
DAI-USDT|SushiSwap-Curve|"10/01/2021| 16:19:19"|0.0040|SushiSwap(0.9926)|Kyber(0.9948)|Curve(0.9966)|UniSwap(0.9997)|DDex(0.9997)|OneSplit(0.9998)
```