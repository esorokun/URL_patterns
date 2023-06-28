import pandas as pd
import datetime
import re
import time
import pytz
import numpy as np
import argparse
import log_rewriter

if __name__ == '__main__':
    log_rewrite('~/Desktop/log_file_full.txt', "~/Desktop/output.csv")