{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "883d661e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import time\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import platform\n",
    "import matplotlib\n",
    "import copy\n",
    "\n",
    "from scipy import stats"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "0d9e392c",
   "metadata": {},
   "outputs": [],
   "source": [
    "pledo = pd.read_excel('pledo.xlsx')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "80f3577b",
   "metadata": {},
   "outputs": [],
   "source": [
    "pledo_cp = copy.deepcopy(pledo)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "92e6db6b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "63366"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "len(pledo_cp)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "29985225",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "미술    19870\n",
       "한글    15339\n",
       "음악    10487\n",
       "요리     6490\n",
       "수학     6291\n",
       "영어     4889\n",
       "Name: 컨텐츠 분류1, dtype: int64"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "pledo_cp['컨텐츠 분류1'].value_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "a2657859",
   "metadata": {},
   "outputs": [],
   "source": [
    "def remove_out(dataframe, remove_col):\n",
    "    dff = dataframe\n",
    "    for k in remove_col:\n",
    "        level_1q = dff[k].quantile(0.25)\n",
    "        level_3q = dff[k].quantile(0.75)\n",
    "        IQR = level_3q - level_1q\n",
    "        rev_range = 1.5  # 제거 범위 조절 변수\n",
    "        dff = dff[(dff[k] <= level_3q + (rev_range * IQR)) & (dff[k] >= level_1q - (rev_range * IQR))]\n",
    "        dff = dff.reset_index(drop=True)\n",
    "    return dff"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "98d637ed",
   "metadata": {},
   "outputs": [],
   "source": [
    "def user_remove_out(dataframe, remove_col):\n",
    "    dff = dataframe\n",
    "    for k in remove_col:\n",
    "        dff = dff[dff[k] <= 600]\n",
    "        dff = dff.reset_index(drop = True)\n",
    "    return dff"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "8dd55c92",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "20"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# 0초인데 정답인 데이터 비율\n",
    "len(pledo_cp[(pledo_cp['문제풀이 소요시간'] == 0) & (pledo_cp['정오답'] == '정답')])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "45f01ac6",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "63366"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "len(pledo_cp)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "5a9758f1",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "========================================IQR 방식 사용========================================\n",
      "① 3Q + (1.5 × IQR) : 34.0\n",
      "② 1Q - (1.5 × IQR) :  : -14.0\n",
      "③ 이상치 제거 전 pledo 크기 :  63366\n",
      "④ 이상치 제거 후 pledo 크기 :  58708\n",
      "⑤ 데이터 손실 크기(율) : 4658(7.35)%\n",
      "====================================사용자 임의 설정 기준====================================\n",
      "① 사용자 임의 설정 기준 최대 : 595\n",
      "② 사용자 임의 설정 기준 최소 : 0\n",
      "② 이상치 제거 전 pledo 크기 :  63366\n",
      "③ 이상치 제거 후 pledo 크기 :  63322\n",
      "⑤ 데이터 손실 크기(율) : 44(0.07)%\n"
     ]
    }
   ],
   "source": [
    "# 이상치 비율 체크해보기 \n",
    "level_1q = pledo_cp['문제풀이 소요시간'].quantile(0.25)\n",
    "level_3q = pledo_cp['문제풀이 소요시간'].quantile(0.75)\n",
    "IQR = level_3q - level_1q\n",
    "\n",
    "pledo_size = len(pledo_cp)\n",
    "pledo_preprocessing_1 = len(pledo_cp[(pledo_cp['문제풀이 소요시간'] <= level_3q + (1.5 * IQR)) & (pledo_cp['문제풀이 소요시간'] >= level_1q - (1.5 * IQR))])\n",
    "pledo_preprocessing_2 = len(pledo_cp[pledo_cp['문제풀이 소요시간'] <= 600])\n",
    "\n",
    "\n",
    "print('=' * 40 + 'IQR 방식 사용' + '=' * 40)\n",
    "\n",
    "print('① 3Q + (1.5 × IQR) : ' + str(level_3q + (1.5 * IQR)) + '\\n' + '② 1Q - (1.5 × IQR) :  : ' + str(level_1q - (1.5 * IQR)))\n",
    "print('③ 이상치 제거 전 pledo 크기 : ', pledo_size)\n",
    "print('④ 이상치 제거 후 pledo 크기 : ', pledo_preprocessing_1)\n",
    "print('⑤ 데이터 손실 크기(율) : {0}({1})%'.format(pledo_size - pledo_preprocessing_1, round(100 * ((pledo_size - pledo_preprocessing_1) / (pledo_size)), 2)))\n",
    "\n",
    "print('=' * 36 + '사용자 임의 설정 기준' + '=' * 36)\n",
    "\n",
    "print('① 사용자 임의 설정 기준 최대 : ' + str(max(pledo_cp[pledo_cp['문제풀이 소요시간'] <= 600]['문제풀이 소요시간'])) + '\\n' + '② 사용자 임의 설정 기준 최소 : ' + str(min(pledo_cp[pledo_cp['문제풀이 소요시간'] <= 600]['문제풀이 소요시간'])))\n",
    "print('② 이상치 제거 전 pledo 크기 : ', pledo_size)\n",
    "print('③ 이상치 제거 후 pledo 크기 : ', pledo_preprocessing_2)\n",
    "print('⑤ 데이터 손실 크기(율) : {0}({1})%'.format(pledo_size - pledo_preprocessing_2, round(100 * ((pledo_size - pledo_preprocessing_2) / (pledo_size)), 2)))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3444835c",
   "metadata": {},
   "source": [
    "<h1> IQR 기준"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 134,
   "id": "2f519d53",
   "metadata": {},
   "outputs": [],
   "source": [
    "pledo_rm = remove_out(pledo_cp, ['문제풀이 소요시간'])"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f80932df",
   "metadata": {},
   "source": [
    "<h1> 10분 기준"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "76ab29a3",
   "metadata": {},
   "outputs": [],
   "source": [
    "pledo_rm = user_remove_out(pledo_cp, ['문제풀이 소요시간'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "95ea86cc",
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'pledo_rm' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-4-c7db49f7ab15>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[0mpledo_rm\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;34m'문제풀이 소요시간'\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mdescribe\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m: name 'pledo_rm' is not defined"
     ]
    }
   ],
   "source": [
    "pledo_rm['문제풀이 소요시간'].describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "c7e88711",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "<ipython-input-10-6359f8227a22>:6: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  pledo_rm['정오답'] = pledo_rm['정오답'].replace('정답', 1).replace('오답', 0)\n"
     ]
    }
   ],
   "source": [
    "# 한글, 영어, 수학 추출\n",
    "pledo_rm = pledo_cp[(pledo_cp['컨텐츠 분류1'] == '한글') | (pledo_cp['컨텐츠 분류1'] == '영어') | (pledo_cp['컨텐츠 분류1'] == '수학')]\n",
    "\n",
    "# 정오답 1과 0으로 변환\n",
    "# 정답 : 1, 오답 : 0\n",
    "pledo_rm['정오답'] = pledo_rm['정오답'].replace('정답', 1).replace('오답', 0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 60,
   "id": "1c867190",
   "metadata": {},
   "outputs": [],
   "source": [
    "korean_course = pledo_rm[pledo_rm['컨텐츠 분류1'] == '한글']\n",
    "math_course = pledo_rm[pledo_rm['컨텐츠 분류1'] == '수학']\n",
    "english_course = pledo_rm[pledo_rm['컨텐츠 분류1'] == '영어']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "id": "383eec44",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "1    12532\n",
      "0     2807\n",
      "Name: 정오답, dtype: int64\n",
      "1    5438\n",
      "0     853\n",
      "Name: 정오답, dtype: int64\n",
      "1    3542\n",
      "0    1347\n",
      "Name: 정오답, dtype: int64\n"
     ]
    }
   ],
   "source": [
    "print(korean_course['정오답'].value_counts()); print(math_course['정오답'].value_counts()); print(english_course['정오답'].value_counts())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 138,
   "id": "685d5fe9",
   "metadata": {},
   "outputs": [],
   "source": [
    "percentage = [18, 28, 14, 82, 72, 86]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "886ea426",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Windows\n"
     ]
    }
   ],
   "source": [
    "print(platform.system()) # 플랫폼 확인\n",
    "\n",
    "# Window\n",
    "if platform.system() == 'Windows':\n",
    "    matplotlib.rc('font', family='Malgun Gothic')\n",
    "elif platform.system() == 'Darwin': # Mac\n",
    "    matplotlib.rc('font', family='AppleGothic')\n",
    "else: #linux\n",
    "    matplotlib.rc('font', family='NanumGothic')\n",
    "\n",
    "# 그래프에 마이너스 표시가 되도록 변경\n",
    "matplotlib.rcParams['axes.unicode_minus'] = False"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 144,
   "id": "3feaeed4",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.legend.Legend at 0x244a8310f10>"
      ]
     },
     "execution_count": 144,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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IC+99BLvvfcew4cPZ9CgQRxxxBFcccUVtfUTJkygb9++9O7dmwcffLC2/cILL2TOnDmlOARJW4FVq1axyy67bFXBDRAR7LLLLs0+o9CkkXdKaTbFh/CnlHbZQNnIBrabT2GSWt22moZqtWU67bTTmDdvHnvvvTczZsxg9OjR3HLLLfzrv/4r5eXlrFmzhkGDBvGb3/yGfv36MW3aNObOncuKFSsYMmQIgwcP5oEHHqBbt27069ev1IcjKWO5B/cFF1zAz372s/XaW3Jc2TykRaWxxx578Pe//529996bJUuWsOeee7LvvvvWri8rK+Pwww/nrbfeIiJYvXo11dXVLF++nB122IGqqiomTpzI9OnTS3gUktR6XnzxRcaMGcOHH34IwPbbb8+Pf/xj9t9/fwBOOOEE1qxZU1t/xBFHMH78eP72t7+1Wh8Mb23UpEmTGDBgAJ/97Gd5//3313tQzptvvsmMGTO49NJL2X777RkxYgSVlZV07dqV8ePHM2rUKG688UY6duxYoiOQtDX6yfzHGi9qhpFHHdOkupqaGoYPH87Pf/5z9ttvPwBeeuklzj77bJ588knatStcjX7kkUca3P7xxx/nC1/4Arvvvvsm9ddnm2uD3nnnHc477zyeeeYZFi5cyJ133smpp55KTU3h5oDf/va3nHLKKdxxxx185jOfAWD48OE8+uijTJ8+nfnz53PkkUeyatUqzjnnHM4880xmzZpVykOSpE3y+uuvs//++9cGN8B+++3H/vvvz+uvv77RbVNKLF68uHbEvikceWuDZs+eTa9evdhnn30AOO6446iuruavf/0rt99+O3/96195+OGH2Xnn9Z+zs2jRIqZOncr9999PZWUlM2bMoH379lRWVjJgwIC2PhRJahV77LEHr7zyCitWrGCHHXYAYMWKFbzyyivsscceAPTv35+LLrqIdu3a1V7Pvvbaa4kITj/99Fbph+GtDTrkkEMYN24cy5YtY8cdd+TFF1+kqqqKp59+mueee26D17FramoYNWoUEydOpF27dixfvrz2/sXq6uq2PARJalUdOnTguuuuY9iwYey9994AvPbaa1x33XW1n3NjxoxpcNsNnUpvCcNbG3TAAQcwbtw4TjjhBDp27EhNTQ133303DzzwAC+88AL9+/evrT3uuOP4/ve/D8BNN93E0KFDWfstcCNHjqSi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qWHcuHH06tWLiooKRo8eTU1NDQATJkygb9++9O7dmwcffLB2HxdeeCFz5swpRfelkrrzzjs5+eSTa4N7zZo1nHPOOcybN49Zs2Y1GNzz589n0aJFnHzyyVx//fVMnjyZiRMnctlll7V196UtgqfNm2n48OEsX76cZcuW1bY9/PDDzJs3j3nz5hERfO1rX2PKlCkMHjyYadOmMXfuXFasWMGQIUMYPHgwDzzwAN26daNfv34lPBKpNKZOncqPf/zj2uVbb72Vrl27MmHChAbrV65cyRVXXMG9997LqlWr+OSTT2jfvj1lZWVUV1e3VbelLYrh3UyTJk2iS5cu9O/fv7Ztt912Y8WKFaxcuZL27duzbNkydt99dyKC1atXU11dzfLly9lhhx2oqqpi4sSJTJ8+vXQHIZXIqlWrePbZZzniiCNq25566imef/75df6fOvPMMxkxYgQAY8aMYcyYMXzqU58C4LjjjqNPnz507NiRH/7wh23af2lLYXg3U5cuXdZrO+KII+jduzc9e/akrKyME088kWOOOQaAESNGUFlZSdeuXRk/fjyjRo3ixhtvXOdan7St6Ny5M++///46bffcc89Gt7nlllvWWR47dixjx45t7a5JWfGadyuYPHkyVVVVvP766yxatIiysjJuvvlmoHCa/dFHH2X69OnMnz+fI488klWrVnHOOedw5plnMmvWrNJ2XpKUHUferWDKlCmMGTOmdjT9ne98h5EjRzJ69OjamkWLFjF16lTuv/9+KisrmTFjBu3bt6eyspIBAwaUqOeSpBw58m4Fhx9+ODNmzKhdnjZtGocddljtck1NDaNGjWLixIm0a9eO5cuX06FDB9q1a+eEG0lSsznybgVXXnklF110EX379gVgn332Wef5zDfddBNDhw6lR48eAIwcOZKKigo6derEJZdcUoouS5Iy5kNatjLb0sMPwIe0SDnalj6nNtdDWhx5S9ooP2ilLY/XvCVJyozhLUlSZgxvSZIyY3hLkpSZbWLC2k/mP1bqLrSZcw8pdQ8kSZubI29JkjJjeEuSlBnDW5KkzBjekiRlxvCWJCkzhrckSZkxvCVJyozhLUlSZgxvSZIyY3hLkpQZw1uSpMwY3pIkZcbwliQpM4a3JEmZMbwlScqM4S1JUmZaFN4R0S0i7omI2RHxWET0jIj9I2JmRMyNiOvr1F4d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\n",
      "text/plain": [
       "<Figure size 576x576 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(8, 8))\n",
    "plt.xticks(fontsize = 12)\n",
    "\n",
    "sns.set_palette(\"Set3\")\n",
    "g = sns.countplot(x = '컨텐츠 분류1', data = pledo_rm, hue = '정오답', order = ['한글', '영어', '수학'], dodge=True)\n",
    "ax = g\n",
    "count = 0\n",
    "\n",
    "for p in ax.patches:\n",
    "    ax.annotate(\"{0}%\".format(percentage[count]), (p.get_x() + p.get_width()/2.,p.get_height() - 30),\n",
    "               ha='center', va='center', fontsize=12, color = 'black', xytext=(0, 10),\n",
    "               textcoords='offset points')\n",
    "    count += 1\n",
    "    \n",
    "plt.xlabel(\"\"); plt.ylabel(\"\"); plt.title(\"문제별 정오답률\", fontsize = 20)\n",
    "plt.legend([\"오답\", \"정답\"])"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2ca7eae3",
   "metadata": {},
   "source": [
    "<h1> 문제별 / 문제풀이 소요시간"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 390,
   "id": "05106f38",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "컨텐츠 분류1\n",
       "수학    16.163194\n",
       "영어    26.075159\n",
       "한글    15.575603\n",
       "Name: 문제풀이 소요시간, dtype: float64"
      ]
     },
     "execution_count": 390,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "a1 = pd.DataFrame(pledo_rm.groupby('컨텐츠 분류1')['문제풀이 소요시간'].mean())\n",
    "a1['문제풀이 소요시간']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 392,
   "id": "2d14618c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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x75vn316OiBQkqSh74EHHnghMye0X9/tpebNGkccSfXNITu1Pj83Io4H3pGZnT5mr6mpKVtaWnpftSRJQ1REPJCZWzzytdtLzRHx9trzcaH6iq0RVPMKd6ut+whwR4c7S5KkzfTkUvM+wBcjYgPVVIyzgZ2BG2rrbsnMrr49RZIk1XQbvJn5PeCQdqsfxwFVkiT1mt/HK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySANh9990HuwRpWBg12AVIGhyXXHIJ11577abl559/ngMOOGDT8sc+9jHOO++8QahMamyRmXU/SFNTU7a0tNT9OFIjWrBgAXfffTfr169n4sSJfOUrX2H8+PE88sgjfPKTn2Tt2rVEBNdccw1TpkzZbN/M5Bvf+Abz58/n3nvvZYcddujwGI8//jh77703Tz31FLvuumuBdyU1voh4IDOb2q/3UrO0ldtnn3248847uffee9l33325+OKLWb9+PccddxwXX3wxq1at4rvf/S577bXXFvsefvjhXH/99bz00kud9r9mzRpOPfVULrroIubMmcMLL7xQz7cjDXteapa2cieeeOKmnw888EBuuOEGli1bRnNzMwceeOCmbRGxxb633norY8aMYfLkyVtse+yxx1i+fDk333wzCxcuZOrUqcyYMYMjjzyS2bNn09zczH777ddhv5L6zjNeaYh44403+Lu/+zuOP/54Vq1axdixY5k1axbTp0/n/PPP54033thinzFjxnTY12uvvcall17KpEmTWLlyJVOnTuXqq6/mkEMO4b777mPKlCksXLiQdevW1fttScOO93ilIeDHP/4xp59+OieeeCJnnHEGM2fOZOLEiVx11VWMHDmS0047jQMOOIBzzz23w/0nT57MQw891Ok9XqhGNT/99NN1egfS8NPZPV4vNUtbuZtuuonLLruMq666in333ReAiRMn0tzczOjRowE44YQTNhuhLGnrZfBKW7HVq1fzqU99iu9///uMHz9+0/rm5mauu+46Zs+ezYgRI7jtttuYNm1aj/s9/fTTaX8Vqv10IoBp06axePHifr0HSZszeKWt2EMPPcQrr7zCMcccs2ndTjvtxPLly/nhD3/IoYceyogRI5g6dSpnnnkmGzduZN68eVxxxRWMGzeu036XLl1aonxJHfAeryRJdeA8XkmStgIGryRJBRm8kiQV5OAqDTvr19852CWoTrbb7vDBLkHqlme8kiQVZPBKklSQwStJUkEGryRJBRm8kiQVZPBKklSQwStJUkEGryRJBRm8kiQVZPBKklSQwStJUkHdPqs5InYAFgMTqYL6VOAY4AzgOeD1zDyijjVKktQwevIlCWOAczPzmYiYBcwHHgMuyMzlda1OkqQG023wZuYzbRZfBl5r87MkSeqFHt/jjYjdqM52vwisBy6OiJURcWYn7edFREtEtKxZs2ZAipUkaajrUfBGxO8BFwKfyMxnMvOqzJwGfBhojoh92++TmUsysykzmyZMmDCwVUuSNET1ZHDVbwFHZ+YZbdaNysw3gQ3AOiDrV6IkSY2jJ4OrZgKHRsSK2vKTwFMRMR3YBrgxMx+uU32SJDWUngyuuhS4tEAtkiQ1PB+gIUlSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQQavJEkFGbySJBVk8EqSVJDBK0lSQaO6axAROwCLgYlUQX0q8DZgEbAtcG9mfrqONUqS1DC6DV5gDHBuZj4TEbOA+cAUYG5mPhER10fEQZm5qq6VSpLUALq91JyZz2TmM7XFl4HXgW0z84nauuXAwfUpT5KkxtLje7wRsRvV2e5lwIttNr0I7NhB+3kR0RIRLWvWrOl3oZIkNYIeBW9E/B5wIfAJqrPeHdps3hHYIlkzc0lmNmVm04QJEwagVEmShr5ugzcifgs4OjPPyMwXM3MdMLp2BgzwEeCOehYpSVKj6MngqpnAoRGxorb8JHAucENEbABuycwf1ak+SZIaSrfBm5mXApd2sMkBVZIk9ZIP0JAkqSCDV5KkggxeSZIKMnglSSrI4JUkqSCDV5KkggxeSZIKMnglSSrI4JUkqSCDV5KkggxeSZIKMnglSSrI4JUkqSCDV5KkggxeSZIKMnglSSrI4JUkqSCDV5KkggxeSZIKMnglSSrI4JUkqSCDV5KkggxeSZIKMnglSSrI4JUkqSCDV5KkggxeSZIKMnglSSrI4JUkqSCDV5KkggxeSZIKMnglSSrI4JUkqSCDV5KkggxeSZIKMnglSSrI4JUkqSCDV5I04HbffffBLmGrNWqwC5AkDX2XXHIJ11577abl559/ngMOOGDT8sc+9jHOO++8Qahs6xOZWfeDNDU1ZUtLS92PI/XE+vV3DnYJqpPttjt8sEsYEu6++24+85nPsGjRok3h+Mgjj/DJT36StWvXEhFcc801TJkyZdM+GzZsYP78+Tz66KO8/PLL7L///lx55ZVss802W/T/+OOPs/fee/PUU0+x6667lnpbW52IeCAzm9qv91KzJA0jp5xyCpdffjlr167dtG79+vUcd9xxXHzxxaxatYrvfve77LXXXpvt99prr3H00Udz++23c//99/P666+zdOnSLfpfs2YNp556KhdddBFz5szhhRdeqPt7Gmq81CxJw8jixYsZM2YMhx122KZ1y5Yto7m5mQMPPHDTuojYbL+ddtqJI444YtO2pqYmnn322U3bH3vsMZYvX87NN9/MwoULmTp1KjNmzODII49k9uzZNDc3s99++23R73DkGa8kDSNjxozZYt2qVasYO3Yss2bNYvr06Zx//vm88cYbnfaxdu1ali1bxrHHHgtUZ8OXXnopkyZNYuXKlUydOpWrr76aQw45hPvuu48pU6awcOFC1q1bV7f3NZQYvJI0zK1evZpHH32UG2+8kRUrVvCzn/2ML33pSx22bWlp4YgjjmDBggW8973vBWDs2LF8+ctf5qSTTmLUqOpC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\n",
      "text/plain": [
       "<Figure size 576x576 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(8, 8))\n",
    "sns.set_palette(\"Set3\")\n",
    "\n",
    "g = sns.barplot(data = a1, x = a1.index, y = a1['문제풀이 소요시간'], order=['한글', '영어', '수학'])\n",
    "ax = g\n",
    "\n",
    "plt.xlabel(\"\"); plt.ylabel(\"\"); plt.ylim(0, 30); plt.title(\"문제별 풀이소요 시간\", fontsize = 20)\n",
    "\n",
    "for p in ax.patches:\n",
    "    ax.annotate(\"{0:,}초\".format(round(p.get_height(), 1)), (p.get_x() + p.get_width()/2.,p.get_height() - 0.2),\n",
    "               ha='center', va='center', fontsize=12, color = 'black', xytext=(0, 10),\n",
    "               textcoords='offset points')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 62,
   "id": "b0f97efc",
   "metadata": {},
   "outputs": [],
   "source": [
    "x1 = pledo_rm[pledo_rm['컨텐츠 분류1'] == '한글']['문제풀이 소요시간']\n",
    "x2 = pledo_rm[pledo_rm['컨텐츠 분류1'] == '영어']['문제풀이 소요시간']\n",
    "x3 = pledo_rm[pledo_rm['컨텐츠 분류1'] == '수학']['문제풀이 소요시간']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "e27eb474",
   "metadata": {},
   "outputs": [],
   "source": [
    "x1 = pledo_cp[pledo_cp['컨텐츠 분류1'] == '한글']['문제풀이 소요시간']\n",
    "x2 = pledo_cp[pledo_cp['컨텐츠 분류1'] == '영어']['문제풀이 소요시간']\n",
    "x3 = pledo_cp[pledo_cp['컨텐츠 분류1'] == '수학']['문제풀이 소요시간']"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "674c56ab",
   "metadata": {},
   "source": [
    "<h1> 한글 IQR"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "2865a0db",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "========================================IQR 방식 사용========================================\n",
      "① 3Q + (1.5 × IQR) : 36.0\n",
      "② 1Q - (1.5 × IQR) :  : -12.0\n",
      "③ 이상치 제거 전 pledo 크기 :  15339\n",
      "④ 이상치 제거 후 pledo 크기 :  14227\n",
      "⑤ 데이터 손실 크기(율) : 1112(7.25)%\n"
     ]
    }
   ],
   "source": [
    "# 이상치 비율 체크해보기 \n",
    "level_1q = pledo_cp[pledo_cp['컨텐츠 분류1'] == '한글']['문제풀이 소요시간'].quantile(0.25)\n",
    "level_3q = pledo_cp[pledo_cp['컨텐츠 분류1'] == '한글']['문제풀이 소요시간'].quantile(0.75)\n",
    "\n",
    "pledo_cp_kr = pledo_cp[pledo_cp['컨텐츠 분류1'] == '한글']\n",
    "\n",
    "IQR = level_3q - level_1q\n",
    "\n",
    "pledo_size = len(pledo_cp_kr)\n",
    "pledo_preprocessing_1 = len(pledo_cp_kr[(pledo_cp_kr['문제풀이 소요시간'] <= level_3q + (1.5 * IQR)) & (pledo_cp_kr['문제풀이 소요시간'] >= level_1q - (1.5 * IQR))])\n",
    "\n",
    "print('=' * 40 + 'IQR 방식 사용' + '=' * 40)\n",
    "\n",
    "print('① 3Q + (1.5 × IQR) : ' + str(level_3q + (1.5 * IQR)) + '\\n' + '② 1Q - (1.5 × IQR) :  : ' + str(level_1q - (1.5 * IQR)))\n",
    "print('③ 이상치 제거 전 pledo 크기 : ', pledo_size)\n",
    "print('④ 이상치 제거 후 pledo 크기 : ', pledo_preprocessing_1)\n",
    "print('⑤ 데이터 손실 크기(율) : {0}({1})%'.format(pledo_size - pledo_preprocessing_1, round(100 * ((pledo_size - pledo_preprocessing_1) / (pledo_size)), 2)))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "d0f5bdcf",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Text(0.5, 1.0, '한글 문제풀이 소요시간 IQR 구간')"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1080x720 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "sns.set_palette(\"Set1\")\n",
    "plt.figure(figsize=(15, 10))\n",
    "\n",
    "sns.histplot(x1, bins= np.arange(100), color='blue', alpha = 0.2)\n",
    "\n",
    "plt.axvspan(xmin = 36, xmax = 100, alpha = 0.2, color = 'red')\n",
    "plt.axvspan(xmin = -12, xmax = 0, alpha = 0.2, color = 'red')\n",
    "\n",
    "plt.ylabel(\"\"); plt.title('한글 문제풀이 소요시간 IQR 구간')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8214c40f",
   "metadata": {},
   "source": [
    "<h1> 영어 IQR"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "003276ec",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "========================================IQR 방식 사용========================================\n",
      "① 3Q + (1.5 × IQR) : 69.5\n",
      "② 1Q - (1.5 × IQR) :  : -30.5\n",
      "③ 이상치 제거 전 pledo 크기 :  4889\n",
      "④ 이상치 제거 후 pledo 크기 :  4548\n",
      "⑤ 데이터 손실 크기(율) : 341(6.97)%\n"
     ]
    }
   ],
   "source": [
    "# 이상치 비율 체크해보기 \n",
    "level_1q = pledo_cp[pledo_cp['컨텐츠 분류1'] == '영어']['문제풀이 소요시간'].quantile(0.25)\n",
    "level_3q = pledo_cp[pledo_cp['컨텐츠 분류1'] == '영어']['문제풀이 소요시간'].quantile(0.75)\n",
    "\n",
    "pledo_cp_en = pledo_cp[pledo_cp['컨텐츠 분류1'] == '영어']\n",
    "\n",
    "IQR = level_3q - level_1q\n",
    "\n",
    "pledo_size = len(pledo_cp_en)\n",
    "pledo_preprocessing_1 = len(pledo_cp_en[(pledo_cp_en['문제풀이 소요시간'] <= level_3q + (1.5 * IQR)) & (pledo_cp_en['문제풀이 소요시간'] >= level_1q - (1.5 * IQR))])\n",
    "\n",
    "print('=' * 40 + 'IQR 방식 사용' + '=' * 40)\n",
    "\n",
    "print('① 3Q + (1.5 × IQR) : ' + str(level_3q + (1.5 * IQR)) + '\\n' + '② 1Q - (1.5 × IQR) :  : ' + str(level_1q - (1.5 * IQR)))\n",
    "print('③ 이상치 제거 전 pledo 크기 : ', pledo_size)\n",
    "print('④ 이상치 제거 후 pledo 크기 : ', pledo_preprocessing_1)\n",
    "print('⑤ 데이터 손실 크기(율) : {0}({1})%'.format(pledo_size - pledo_preprocessing_1, round(100 * ((pledo_size - pledo_preprocessing_1) / (pledo_size)), 2)))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "4b824a6f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Text(0.5, 1.0, '영어 문제풀이 소요시간 IQR 구간')"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1080x720 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "sns.set_palette(\"Set1\")\n",
    "plt.figure(figsize=(15, 10))\n",
    "\n",
    "sns.histplot(x2, bins= np.arange(100), color='red', alpha = 0.2)\n",
    "\n",
    "plt.axvspan(xmin = 69.5, xmax = 100, alpha = 0.2, color = 'red')\n",
    "plt.axvspan(xmin = -30.5, xmax = 0, alpha = 0.2, color = 'red')\n",
    "\n",
    "plt.ylabel(\"\"); plt.title('영어 문제풀이 소요시간 IQR 구간')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b4fcd013",
   "metadata": {},
   "source": [
    "<h1> 수학 IQR"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "615a723e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "========================================IQR 방식 사용========================================\n",
      "① 3Q + (1.5 × IQR) : 38.5\n",
      "② 1Q - (1.5 × IQR) :  : -13.5\n",
      "③ 이상치 제거 전 pledo 크기 :  6291\n",
      "④ 이상치 제거 후 pledo 크기 :  5809\n",
      "⑤ 데이터 손실 크기(율) : 482(7.66)%\n"
     ]
    }
   ],
   "source": [
    "# 이상치 비율 체크해보기 \n",
    "level_1q = pledo_cp[pledo_cp['컨텐츠 분류1'] == '수학']['문제풀이 소요시간'].quantile(0.25)\n",
    "level_3q = pledo_cp[pledo_cp['컨텐츠 분류1'] == '수학']['문제풀이 소요시간'].quantile(0.75)\n",
    "\n",
    "pledo_cp_mt = pledo_cp[pledo_cp['컨텐츠 분류1'] == '수학']\n",
    "\n",
    "IQR = level_3q - level_1q\n",
    "\n",
    "pledo_size = len(pledo_cp_mt)\n",
    "pledo_preprocessing_1 = len(pledo_cp_mt[(pledo_cp_mt['문제풀이 소요시간'] <= level_3q + (1.5 * IQR)) & (pledo_cp_mt['문제풀이 소요시간'] >= level_1q - (1.5 * IQR))])\n",
    "\n",
    "print('=' * 40 + 'IQR 방식 사용' + '=' * 40)\n",
    "\n",
    "print('① 3Q + (1.5 × IQR) : ' + str(level_3q + (1.5 * IQR)) + '\\n' + '② 1Q - (1.5 × IQR) :  : ' + str(level_1q - (1.5 * IQR)))\n",
    "print('③ 이상치 제거 전 pledo 크기 : ', pledo_size)\n",
    "print('④ 이상치 제거 후 pledo 크기 : ', pledo_preprocessing_1)\n",
    "print('⑤ 데이터 손실 크기(율) : {0}({1})%'.format(pledo_size - pledo_preprocessing_1, round(100 * ((pledo_size - pledo_preprocessing_1) / (pledo_size)), 2)))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "67120579",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Text(0.5, 1.0, '수학 문제풀이 소요시간 IQR 구간')"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAA2sAAAJaCAYAAACx5N8sAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjUuMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8qNh9FAAAACXBIWXMAAAsTAAALEwEAmpwYAAAumUlEQVR4nO3dfZhnZ10f/vdHEqBgbLIPCRqLoZYLr0ARdAmCkwTFpjTCajG/+lBFLZqwV7Gt+FxpRRFqjVZUNCW1FKs2KOLD1kaU0AZ2QSihYkVkd2mJKVLtJgshGAwJ8/n98f0ufjP7nd3Z3Xm4Z+b1uq69mHPu+5zzmclh9vve+z73qe4OAAAAY/m0jS4AAACAEwlrAAAAAxLWAAAABiSsAQAADEhYAwAAGJCwBrDFVNVFVfWFS/ZdUFWXrnMdj6qqS9bw/JdU1aPW6vxnq6rOr6rPO43+T6qqh69lTetprf/7A2wH52x0AQCsTFV9b5K/7O5XnKLrk5Nck+RbZvZ9fpJvmv452TUWkuxPcseSpocmuaO7n7WCOr8pyWcn+WCSS5K8ZKbtp5I8/SSHf0N3//GprjH1TUluT/KaFfZfb0/Kkp95Vf23JBfM9Lk0yXndfV+SV+SvvqcNU1X/Oskz5zTtTPLvuvvlM32/Pck3zvT57CTf290/l+RZWfLfH4DTI6wBbB5XJfl4Jh/qH2Q6avafppsPSXJOVb17uv1vk7zvNK6zv7u/acn5/1aSVy7Z9y+TPDfJRUnuT3Jseq2/XO7E3f1PquoLklzV3T8yPc9FSf55d//TOd/XY5PcmElQuCvJtd195DS+l9lzVZJj3X3BKfo9Ocn3JHlsksVMfp6Hk/yr7v6DZY65Jcm3dPftJzt3d3/JzDGfneS3pkFtGN39PfP2V9U/SnLhkr4/keQnZvrckuS2NS0QYBsxDRJgcFX1iKr62ST/M8n7q+onq+qRs326+73d/aQk+5L85yS/k+TfJHlKd//btairu39oes2fSfJD3f2kFV7r05Lsmdl+VJJHL+00DVe/kuTF3f3EJN+f5HVVdaZ/d12T5Peq6iuX61BVn5nkNzMZQfrC7n5Kd39Bklcn+c9VdeFyh07/nI4XJHntSjtPp32+e2a7quqFVfXfq+ptVfX7VXVTVT16ps9Lqur9VXVrVb2jql5dVQ87zTqPe0gmoXy5+h6X5FHd/e7l+gBweoQ1gEFV1VOmo1dvT/IH3f3PpqNP707y5qr6V1V1xUz/vUm+L5MRth9Pcn6Sn5855d6qendVfdkpLv3sqrpt9k+SXz9J//OSPLKqzq2q85M84iTf069nMvp2ycy5/32SvzHdvmqm+5OS3N7db02S7n5bkv+V5CmnqH/edb96etyXJ3l6VX3NMl0/P8nbu/tNszu7+3czGTH628sc91lJLj6Ner4gyT/IktHKTMLof1zhaX48yeVJntndT+/uJyf5hSRvrKpdM/1e2d3P6O6nJvlEkn+80jqXeFiSe+c1VNW5mfx3/P4lTf+oqg5OgxwAp8k0SIBx7crk2bEv7u57ju/s7v9QVf8pyZckmZ1Cd0WSX+ju9yRJVd2Q5Ntm2k+Y3rhUdx+cXvd0fF6SR2byLNr3ZRJafnmZ8//90zjvo5McWrLvfUk+J8k7TnVwVX16kq9L8neT/HZ3f/e06bur6hur6nVJbknyi939F9O2/57kJ6vqmbOBbRoiH5/kXXOu85nTWp+Z5OAK6tqTyYjh13X3x5Y0f3uS/72Cc3x2JlNQL+3uTwWo7r65qp6W5IWZ/6zYwSRfdKrzL+MzcuKzjKmqR2Ty3/sd3f2bS5p/LZNpux86w2sCbGvCGsCguvu3T9J2X5I3LNn96iQ3VdVlST6ayTNuP73S681OsTuFV04XkEhV7chkUYnPSvJPu/tZMwuMLD3/0meZHpHkMzMZLZv1s9396kyegfvrS9rOn+5fiXuT/Hkmi5bcO63hJd39ku7++ar65UwC1sePH9Ddx6rq2Un+Z1X9YSYLq5yT5HOTPLG7PzLnOt+e5DuS/OOqemV33zWvmKp6aCbTVL9jWtPb53T7YHevJNg8NclbZ4PajLdMa1p6/U/PZAGT65epb2+SH1qy+7My+Xn/ZSY/h8Wq+s5Mnjn8f9MFaX4yyX9L8l1zTvuRUz3HB8DyhDWAAU2X3n/Vkt0XZbLgxdEl+5/f3X/Q3e+tqqcm+cJMgtDPdff/nfb500xGkZY1ff5stobPzmTU6RknOey7k/zstLZrk9xwkvPvqaoLMplqmCSPS/INSV483b67u39/5pB3J/nZqnpYd983fdbqGTP9T6q7FzN5/mzWt2Q64tTdf5nkv8w59P8k+ZPuvuz4jqp633T/g1TVl06/n+/J5Gd8U1XtnZ57qb+X5MokC919wgjVaTonSS/TtpgHP1v2wqp6XiYrMz6vu39n3kHdvT+TlUA/pap+NcmPdPcJi4ZMw99LM3lecenPGYBVIKwBDKi735UHL8KR6YjGX3b30uecZt2YyXLwx4+ZbfuNU113uvriru7+vRX0/ZJMptR9f5K/lsmzUqc67hGZTJs87hen25+RZG+SheMN3X1PVf14kjdU1W8m+cok/6a7P3yq2tZDVX1VJtM+/253dyYLkDw6k+cJF5b2nwaa36yqr66qj3T3R8/i8rcl+ddV9fA5wfDKTKZzHvfKTEa/vjmTKaBv6O4HzuLaSZLpFM4vqarHV9XTp88UArCKhDWALaS7nzdvf1U9I8nXr+AUX5jJwh6/l8lS+T9wkr7XJPmH3f3JJB+bTn/8W6c4/8V58PvfjjsnydLnt9Ldr6mqW5M8Mck3d/cHTnH+T6mqn8uSwJvkwjnTPd/e3S+Y6V+ZLIAy2++SJO+oqj7eP8kfZzId8FPTMrv7Z6rq5u6+f0lQnrUvk2fuHhTWTjGC+SDd/b+q6neS/Luqum5mmufeJF+byTTJ2f6d5NXThU1+MCcuBHI2npLJz+dBYa27X7OK1wDYloQ1AObq7o8nefNJ2v/xku1DSQ5NQ9tyPiPJbdOws9I6bs8ZvCi6u+eFwtXs/95l9q84UJ6l48+/Haiq46NrT0zy8tkAucR3Jbmtqm7p7v+2HkUCcOaENQCW+uaqeta8hqXPtZ2ha6pquRUJL59d+XILu7mqPjFn//Xd/UvzDpiG1ifNbC9msljIpxYMqcnLy//TdMXJF3T3S5ac4+OZrGq52l5Q899fd6i7v3oNrgewLdRkZgQAo5t+EP/kmYzcVNU5Sc6dflhfF9PVDz9tmcU2VuP8D0+y2N3zQs+Gm/7MH7rMio2bQlWdl+Tjq/GMGwCnT1gDAAAY0KdtdAEAAACcaEOfWdu1a1dfcsklG1nCfH/xF8knP7nRVWx9D3lI8shHbnQVwEby+xaA9TLoZ893vetdd3b37nltGxrWLrnkktx22wnv2dx4b3hDsnvuz4vVdPRo8qy5axgA24XftwCsl0E/e1bVnyzXZhokAADAgIQ1AACAAQlrAAAAAxLWAAAABiSsAQAADEhYAwAAGJCwBgAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBAwhoAAMCAhDUAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIGENAABgQOdsdAEwsr17r86xY3eesH/Hjl3Zv//mDagIAIDtQliDkzh27M4cPHjDCfsXFvZtQDUAAGwnpkECAAAMSFgDAAAYkLAGAAAwIGENAABgQMIaAADAgIQ1AACAAQlrAAAAA/KeNTgDhw4dzsLCZXPbvDAbAIDVIKzBGVhcvH/uy7ITL8wGAGB1mAYJAAAwIGENAABgQMIaAADAgIQ1AACAAQlrAAAAAxLWAAAABiSsAQAADEhYAwAAGJCwBgAAMCBhDQAAYEDCGgAAwICENQAAgAGtOKxV1buq6llV9aiq+q2qOlBVr6mqc6ft+6rqLVX1jqq6cu1KBgAA2PpWFNaq6pok5083X5bk5d19eZKjSZ5bVZ+T5DlJrkyyN8n1q18qAADA9nHOqTpU1XlJviHJL013Pa673zb9+vVJvibJpyd5XXd3kj+vqmNVdX53f2QNagYAANjyVjKy9lNJfjjJ4pxj7kpyQZILMxllW7r/BFV1bVXdVlW3HT16dF4XAACAbe+kYa2qvj7JHd39ztndM19fkElIuzsPDmfH95+gu2/s7j3dvWf37t1nVjUAAMAWd6qRta9NcmlVvTbJNUm+N8mfVdUXTNu/KsktSQ5Mv05VXZjknO7+2NqUDAAAsPWd9Jm17v7y419X1UuSvD3JkSSvrqrFJO9M8jvd3VX1+1X1tiQfT/LP1qxiAACAbeCUC4wc190vmdk8YWn+7v7BJD+4CjUBAABse16KDQAAMCBhDQAAYEArngYJW9XevVfn2LE757YdOXJ4nasBAIAJYY1t79ixO3Pw4A1z23buvGKdqwEAgAlhDVbZoUOHs7Bw2dy2HTt2Zf/+m9e5IgAANiNhDVbZ4uL9y47ULSzsW+dqAADYrCwwAgAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBAwhoAAMCAhDUAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIGENAABgQMIaAADAgIQ1AACAAQlrAAAAAxLWAAAABiSsAQAADEhYAwAAGJCwBgAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBAwhoAAMCAhDUAAIABnbPRBcB62Lv36hw7dufctiNHDq9zNQAAcGrCGtvCsWN35uDBG+a27dx5xTpXAwAAp2YaJAAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBAwhoAAMCAhDUAAIABnXOqDlX10CSvT3JekkrydUn+vyTXJfnzJJ/o7qumfV+a5Irpea/t7j9ao7oBAAC2tFOGtSQPJPnq7r63qr4+yTcmuTfJi7v79cc7VdXlSS7q7iur6glJrk9y9VoUDQAAsNWdchpkdy92973Tzccm+cPp1x9e0vWqJDdNj3lPkh2rVSQAAMB2s6Jn1qrqu6rqSJI9Sf5rko8neXlVHaiqF0y7XZjk6MxhD1TVCeevqmur6raquu3o0aNLmwEAAMgKw1p3X9/dj03yyiQ/092v6u4vSvJ3knxlVT0+yd1JLpg5bLG7F+ec68bu3tPde3bv3r0K3wIAAMDWc8qwVlXnVVVNN+9I8ulVdfxZt/syeX6tkxxIcs30mEuTfHD1ywUAANgeVrLAyOcleUVV3ZfJ9McXJvnBqlpIcm6SX+vu91bV+5JcXVUHktyTyWqRwIxDhw5nYeGyE/bv2LEr+/ffvAEVAQAwqlOGte5+Z5IvXrL7++f0W0yyb5Xqgi1pcfH+HDx4wwn7Fxb8XwcAgAfzUmwAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIGENAABgQMIaAADAgIQ1AACAAQlrAAAAAxLWAAAABiSsAQAADEhYAwAAGJCwBgAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBAwhoAAMCAhDUAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIGENAABgQMIaAADAgIQ1AACAAQlrAAAAAxLWAAAABiSsAQAADEhYAwAAGJCwBgAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBAwhoAAMCAhDUAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAY0Dmn6lBVD03y+iTnJakkX5fk05P8bJKHJ3lbd3/XtO9Lk1wxPe+13f1Ha1Q3AADAlnbKsJbkgSRf3d33VtXXJ/nGJJcneX53315Vr6uqpyZ5aJKLuvvKqnpCkuuTXL1mlQMAAGxhp5wG2d2L3X3vdPOxSf4wycO7+/bpvtcneVqSq5LcND3mPUl2rHq1AAAA28SKnlmrqu+qqiNJ9iT5H0nummm+K8kFSS5McnRm/wNVdcL5q+raqrqtqm47evTo0mYAAACywrDW3dd392OTvDLJTyQ5f6b5gkxC2t3Tr49b7O7FOee6sbv3dPee3bt3n3HhAAAAW9kpw1pVnVdVNd28Y3rMw6rq4um+5ya5JcmBJNdMj7k0yQdXv1wAAIDtYSULjHxekldU1X1JPp7khUl2JfnV6b793f2+qjqc5OqqOpDkniTXrVXRAAAAW90pw1p3vzPJFy/Z/YFMFhWZ7beYZN/qlQYAALB9eSk2AADAgIQ1AACAAQlrAAAAAxLWAAAABiSsAQAADEhYAwAAGJCwBgAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBAwhoAAMCAhDUAAIABCWsAAAADEtYAAAAGdM5GFwAkhw4dzsLCZXPbduzYlf37b17nigAA2GjCGgxgcfH+HDx4w9y2hYV961wNAAAjMA0SAABgQMIaAADAgIQ1AACAAQlrAAAAA7LACFvG3r1X59ixO+e2HTlyeJ2rAQCAsyOssWUcO3bnsisq7tx5xTpXAwAAZ8c0SAAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBAwhoAAMCAhDUAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIGENAABgQMIaAADAgIQ1AACAAQlrAAAAAxLWAAAABiSsAQAADEhYAwAAGJCwBgAAMCBhDQAAYEDCGgAAwIDO2egCgJM7dOhwFhYum9u2Y8eu7N9/8zpXBADAehDWYHCLi/fn4MEb5rYtLOxb52oAAFgvpwxrVXV+kn+b5FGZTJv8xiRfkeS6JH+e5BPdfdW070uTXDE977Xd/UdrUzYAAMDWtpKRtUckeVF3f6iqvjzJdyY5kuTF3f36452q6vIkF3X3lVX1hCTXJ7l6LYoGAADY6k4Z1rr7QzObH07yFzNfz7oqyU3TY95TVTvmna+qrk1ybZI8+tGPPt16AQAAtoUVrwZZVRdnMqr2iiQfT/LyqjpQVS+YdrkwydGZQx6oqhPO3903dvee7t6ze/fuM68cAABgC1vRAiNV9ewkz0nyrd19V5JXJXlVVT08yW9U1YEkdye5YOawxe5eXO2CAQAAtoNTjqxV1ROTPKe7r5sGtVTV8ZB3X5J7k3SSA0mumbZfmuSDa1IxAADANrCSkbVnJbm8qm6dbt+R5P9U1UKSc5P8Wne/t6rel+Tq6SjbPZmsFgkAAMAZWMkCIz+a5EdX0G8xiZc+AQAArIIVLzACAADA+hHWAAAABiSsAQAADEhYAwAAGJCwBgAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABjQORtdAJyuvXuvzrFjd56w/8iRwxtQDQAArA1hjU3n2LE7c/DgDSfs37nzig2oBgAA1oZpkAAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBAwhoAAMCAhDUAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIGENAABgQMIaAADAgIQ1AACAAQlrAAAAAzpnowsAztyhQ4ezsHDZ3LYdO3Zl//6b17kiAABWi7AGm9ji4v05ePCGuW0LC/vWuRoAAFaTaZAAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIGENAABgQJbuhy1quXewef8aAMDmIKzBFrXcO9i8fw0AYHMwDRIAAGBAwhoAAMCAhDUAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIGENAABgQMIaAADAgIQ1AACAAQlrAAAAAzplWKuq86vqtVV1a1W9paoeU1WPq6o3VdVbq+r6mb4vrao3T/c/fm1LBwAA2LrOWUGfRyR5UXd/qKq+PMl3JvmbSZ7f3bdX1euq6qlJHprkou6+sqqekOT6JFevWeUAAABb2CnDWnd/aGbzw0k+keTh3X37dN/rkzwtyc4kN02PeU9V7VjdUgEAALaPFT+zVlUXZzKq9mNJ7pppuivJBUkuTHJ0Zv8DVXXC+avq2qq6rapuO3r06NJmAAAAssKwVlXPTvIvk3xrJqNr5880X5BJSLt7+vVxi929uPRc3X1jd+/p7j27d+8+07oBAAC2tJUsMPLEJM/p7uu6+67uvjfJw6YjbUny3CS3JDmQ5JrpMZcm+eAa1QwAALDlrWSBkWclubyqbp1u35HkRUl+taruS7K/u99XVYeTXF1VB5Lck+S6tSgYAABgO1jJAiM/muRH5zQ9bUm/xST7VqkuAACAbc1LsQEAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBAwhoAAMCAhDUAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIGENAABgQMIaAADAgIQ1AACAAQlrAAAAAxLWAAAABiSsAQAADOicjS4AWF+HDh3OwsJlc9t27NiV/ftvXueKAACYR1iDbWZx8f4cPHjD3LaFhX3rXA0AAMsxDRIAAGBAwhoAAMCAhDUAAIABCWsAAAADssAI8ClWigQAGIewBnyKlSIBAMZhGiQAAMCAhDUAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIGENAABgQMIaAADAgIQ1AACAAQlrAAAAAxLWAAAABiSsAQAADEhYAwAAGJCwBgAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADCgcza6AGBzOHTocBYWLjth/44du7J//80bUBEAwNYmrAErsrh4fw4evOGE/QsL+zagGgCArc80SAAAgAEJawAAAAMS1gAAAAZ0yrBWVbur6mVV9dLp9j+rqj+uqlur6ndn+r20qt5cVW+tqsevZdEAAABb3UoWGPnxJO9P8oiZfS/u7tcf36iqy5Nc1N1XVtUTklyf5OpVrRQAAGAbOeXIWnc/L8lbluz+8JLtq5LcNO3/niQ7ljtfVV1bVbdV1W1Hjx49zXIBAAC2hzN5Zu3jSV5eVQeq6gXTfRcmmU1eD1TV3HN3943dvae79+zevfsMLg8AALD1nXZY6+5XdfcXJfk7Sb5y+nza3UkumOm22N2Lq1QjAADAtnPaYa2qjj/ndl+Se5N0kgNJrpm2X5rkg6tVIAAAwHa0kgVGlvrBqlpIcm6SX+vu91bV+5JcXVUHktyT5LrVLBIAAGC7WVFY6+5bk9w6/fr757QvJtm3moUBAABsZ16KDQAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBAwhoAAMCAhDUAAIABCWsAAAADEtYAAAAGJKwBAAAM6JyNLgDYuvbuvTrHjt05t23Hjl3Zv//mda4IAGDzENaANXPs2J05ePCGuW0LC/vWuRoAgM3FNEgAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIEv3A2fl0KHDWVi4bG7bkSOH17kaAICtQ1gDzsri4v3Lvktt584r1rkaAICtwzRIAACAAQlrAAAAAxLWAAAABiSsAQAADEhYAwAAGJCwBgAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAzonI0uANieDh06nIWFy07Yv2PHruzff/MGVAQAMBZhDdgQi4v35+DBG07Yv7CwbwOqAQAYj2mQAAAAAxLWAAAABiSsAQAADEhYAwAAGJCwBgAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAYkrAEAAAxIWAMAABiQsAYAADAgYQ0AAGBApwxrVbW7ql5WVS+dbj+uqt5UVW+tqutn+r20qt483f/4tSwaAABgq1vJyNqPJ7kvybnT7VckeX53f3GSS6rqqVV1eZKLuvvKJNcluX7umQAAAFiRU4a17n5ekrckSVWdm+Th3X37tPn1SZ6W5KokN037vyfJjrUoFgAAYLs43WfWdiW5a2b7riQXJLkwydGZ/Q9U1dxzV9W1VXVbVd129OjReV0AAAC2vdMNa3cnOX9m+4JMQtrd06+PW+zuxXkn6O4bu3tPd+/ZvXv3aV4eAABgezitsNbd9yZ5WFVdPN313CS3JDmQ5JokqapLk3xwNYsEAADYbs45g2NelORXq+q+JPu7+31VdTjJ1VV1IMk9mSwyAgAAwBlaUVjr7luT3Dr9+p2ZLCoy276YZN8q1wYAALBteSk2AADAgIQ1AACAAQlrAAAAAxLWAAAABiSsAQAADOhMlu4HWDOHDh3OwsJlc9t27NiV/ftvXueKAAA2hrAGDGVx8f4cPHjD3LaFBW8IAQC2D9MgAQAABiSsAQAADEhYAwAAGJCwBgAAMCALjDCkvXuvzrFjd85tO3Lk8DpXAwAA609YY0jHjt257IqAO3desc7VAADA+jMNEgAAYEDCGgAAwICENQAAgAEJawAAAAMS1gAAAAZkNUhgSzjZ6x527NiV/ftvXueKAADOjrAGbAkne93DwsK+da4GAODsmQYJAAAwIGENAABgQMIaAADAgDyzBmwahw4dzsLCZXPbjhw5vM7VAACsLWEN2DQWF+9fdhGRnTuvWOdqAADWlmmQAAAAAxLWAAAABiSsAQAADMgza8C2tXfv1Tl27M65bTt27Mr+/Tevc0UAAH9FWAO2rWPH7lx2wZKFhX3rXA0AwIOZBgkAADAgI2vAlrfc+9m8mw0AGJmwBmx5y72fzbvZAICRmQYJAAAwIGENAABgQMIaAADAgDyzBnCalns/m3ezAQCrSVgDOE3LvZ/Nu9kAgNVkGiQAAMCAjKwBbDDTKgGAeYQ1gDmWe5F2svov0zatEgCYR1gDmGO5F2knXqYNAKwPz6wBAAAMSFgDAAAYkLAGAAAwIGENAABgQMIaAADAgKwGCbBKTrbcv3emAQCnS1gDWCUnW+7fO9MAgNNlGiQAAMCAhDUAAIABCWsAAAAD8swawCa0d+/VOXbszrltFjMBgK1BWAPYhI4du9NiJgCwxZ1VWKuq/5vk0HTzxiTvSvKzSR6e5G3d/V1nVx4AAMD2dLYja+/v7mcc36iq307y/O6+vapeV1VP7e53nOU1AAAAtp2zXWDkw8e/qKpzkzy8u2+f7np9kqctPaCqrq2q26rqtqNHj57l5QEAALamsw1rj66qN1fV65J8VpK7ZtruSnLB0gO6+8bu3tPde3bv3n2WlwcAANiazmoaZHc/KUmq6kuS/FiS82eaL0hi6AxgnR06dDgLC5fNbbNSJABsHmcc1qrqId39yenmh5N0kodV1cXd/adJnpvkJWdfIsDmd7IAdeTI4VW91uLi/VaKBIAt4GxG1h5dVb+U5L4kn0iyL8nOJL9aVfcl2d/d71uFGgE2vZMFqJ07r1jnagCAzeCMw1p3fyDJ05fs/t+Zs6gIAGNYboTP9EgAGI+XYgNsI8uN8JkeCQDjEdYABrWez7kBAOMR1gAG5Tk3ANjezvY9awAAAKwBYQ0AAGBAwhoAAMCAhDUAAIABCWsAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIGENAABgQMIaAADAgIQ1AACAAQlrAAAAAxLWAAAABiSsAQAADOicjS4AgI136NDhLCxcNrdtx45d2b//5nWuCAAQ1gDI4uL9OXjwhrltu3c/c9kg94EPfCCPecxjTtgv4AHA2RPWADipkwW5nTuvmNu2sLBvrcsCgC3PM2sAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGAAAwIKtBArApfPu3/5N89KMfOWH/Z3zG+fmJn/ip9S8IANaYsAbApvDRj34k//7ff98J+5///H+1AdUAwNozDRIAAGBAwhoAAMCATIMEYNUdOnQ4CwuXzW37wAc+kMc85jFJksuOfSR3P/TcT7Wt9vNnyz3nliR/+qcfysUXf9YJ+0eoYS3qAGDzEdYAWHWLi/fn4MEb5rbt3HnFX7W94W3J7gs+1bbaz58t95xbknzpl37rujwDdyY1rEUdAGw+pkECAAAMyMgaAMO4/U/uyPOf/7y5bXfcccc6VwMAG0tYA2AYvfjASacMcuZO9uyc5+MAxiSsAcA2cLJn5zwfBzAmYQ0AVsjoFADrSVgDgBmnem7ujW+cv8ql0SkAVpuwBgAzPDcHwCiENQA2NStIArBVCWsAbGrbcSRsuWfnPDcHsLUIawCwySy3sqPn5gC2FmENAFbBctMxN8NUzOVqP9ORuvVcNdMoI7CVCWsAsAqWm465GaZiLlf7mY7Urec73YwyAluZsAYAzHWyxVtGH7k609qN1AEjEdYAgLlOtnjLao9crfbUyTOtfbmRumd+2b5NG1yBzUtYA4ABbdVXEpzs2b6RXzh+svAnyAFrRVgDgAGdySsJNkPAG+HZvtX+Oa3nCORmtp4Lz4xgu32/rA1hDQC2iO34zrkz4ee0MdZz4ZkRbLfvl7UhrAEAQ9sMI4YAa0FYAwBO23oGqO02Enay6XN/+qcfysUXf9bctjOZWmeqHoxNWAMATtt2C1BrYbmgdLLFVr70S7/1tKfWnSyQjb6wy8kImivjdRSbm7DGhvmBl/yLvOmH/+XctiNHDq9zNQCwvpZ7pmm1w+7Jnp06k2uNEpJO9n0tt0Lnao9MbgZeHL+5rXpYq6qXJrlieu5ru/uPVvsabA33fPTuHHzvTXPbdu68Yp2rAYDVt57TRU/2WoTVPt9qj8Ytd60zDVAnW3X0TBb9OJOpqSf7uZ/svljufGfyMveT1bGZX3o/yj8YrIdVDWtVdXmSi7r7yqp6QpLrk1y9mtcAANgs1nO66Gq/FmE9X7Ow3LVGGf051ejk6f6cTnVfnO7P4kxGTzfzKye200qbqz2ydlWSm5Kku99TVTtW+fwAAGwTVgLdGGcy8neytjM55mRt2+m/fXX36p2s6lVJfrq73zPdPpjkiu5enOlzbZJrp5uPS3Jo1Qpgs9mV5M6NLoLhuC9YjnuDedwXzOO+YJ5R74vP6e7d8xpWe2Tt7iQXzGwvzga1JOnuG5PcuMrXZROqqtu6e89G18FY3Bcsx73BPO4L5nFfMM9mvC8+bZXPdyDJNUlSVZcm+eAqnx8AAGBbWO2Rtf+S5OqqOpDkniTXrfL5AQAAtoVVDWvTKY/7VvOcbGmmwzKP+4LluDeYx33BPO4L5tl098WqLjACAADA6ljtZ9YAAABYBcIaAADAgIQ1NkRVvbSq3lxVb62qx290PWyMqjq/ql5bVbdW1Vuq6jFV9biqetP03rh+o2tkY1XVu6rqWVX1qKr6rao6UFWvqapzN7o2NkZVXTb9ffHWqvpuvzNIkqr6jqp6x/Q+eLL7Yvuqqt1V9bKqeul0e+69sFk+i672apBwSlV1eZKLuvvKqnpCkuuTXL3BZbExHpHkRd39oar68iTfmeRvJnl+d99eVa+rqqd29zs2tkw2QlVdk+T86ebLkry8u982/cv2uUl+eaNqY2NMQ/oPJPmK7v7wdN9vx++Mba2qLkryFUm+KMnnJvmJTD7jui+2px9P8v5MPmMkySuy5F5I8tBsks+iRtbYCFcluSlJuvs9SXZsbDlslO7+UHd/aLr54SSfSPLw7r59uu/1SZ62EbWxsarqvCTfkOSXprse191vm37tvti+/l6S25PcNP2X8qfG7wySe6f/+9Aku5LcGffFttXdz0vyluRT/8Az717YNJ9FhTU2woVJjs5sP1BV7sVtrKouzmRU7ceS3DXTdFeSCzakKDbaTyX54SSL0+3Z3xHui+3rsZl8qHp2kucneW38ztj2uvueTD6c/3GS/UleHfcFE7sy/17YNJ9FTYNkI9ydB//SXJy+o49tqKqeneQ5Sb41ycfzV9Peksl9cnTOYWxhVfX1Se7o7ndOp8cmSc10cV9sXw8k+d3ufiDJ7VX1kTz47xP3xjY0/T1xbiZTIC/IZPRk9nOF+2L7ujvzP1f8tWySz6JDJki2vANJrkmSqro0yQc3thw2SlU9Mclzuvu67r6ru+9N8rDpSFsyeS7plo2rkA3ytUkurarXZvK74nuT/FlVfcG0/avivtiufi+TqZDHn1O6O8lD/c7Y9j4nyZ/35OXBH01yXpId7gtO8rli03wWNbLGRvgvSa6uqgNJ7kly3QbXw8Z5VpLLq+rW6fYdSV6U5Fer6r4k+7v7fRtVHBuju4+PpqWqXpLk7UmOJHl1VS0meWeS39mY6thI3f3fq+pQVb01k1G2F2XyD89+Z2xvr8nk98ObkzwsyauSvDvuCyZO+FxRVYezST6L1uQfIQAAABiJaZAAAAADEtYAAAAGJKwBAAAMSFgDAAAYkLAGwLCq6ryq+pJVPN/FVbVntc53FnV8xQr6PLmqXrQe9QAwJmENgDU1XWr91iV/3r+kzy1V9a6qOjL9+vOr6g1Jdib5hzP9nlpVB6rqvmm/W6rqL6vqrVX19Jl+j6iqX6yqt1TVb1TVrmnTYzN5ZcRK6v4fJ2mrqnpxVb25qt44/d8XV1XN6fs1VfVNS3Z/20z745b8bO6YNj0syWespFYAtibvWQNgrX2gux8UkKZB7FO6+8uq6hlJvqi7f2TaZ965bkvynCQ/n+Srp/tem+Rbknx4pt8/TfJfu/vVVfWlSX44yQtWWvD0JalPrqondPd75nR5YSZ/hz6ju3sa0n5guv+nl/R9yPTPXN19KMkzptf93CQvW2mdAGxtwhoAa+2Sqrplyb7PmdNvZ5Lzq+oJSZ6U+aNKe5L8/SR/nOQl033vS/KdSX4zye9N9z09yVcmSXf/16r6npUWW1V/Pcl/SPJDmbxo96ru/siSbk9J8oM9fVnpNLD9QiaBbam/keQRK7z8y5P8m5ntJ1TV3+/uX19p/QBsHcIaAGuquz9vhV2fnOQJSRaTPJCkZxur6plJvu8kx++pqh/t7t+dXLY/OdP2yeUOmjn/OUmeneTFSX60u3+lqv5nkluq6uVJ9nf3A9Pub0zy3VX1Hd39sao6b1rbG+ec+ookDz3FtSvJjyT5/e5+x6lqBWB7ENYAWBNV9XeSfP/Mrodk8qz0/TP7fqS73zANSk9OcnuSj3X3a5c+59Xdb0rypqq6cHqer8rk77FfTrLY3f9vpvvHqmpHdx+rqnOzsme0/3aSpybZ290fqqqndvfrq+pgJtMb/1eSP5jW8gvTRUJ+q6oWk1SSu7r7F5b8DJ6T5B1J/l9VvbC7Xznn5/SkTEbx3tjdS6dQvseoGsD2JawBsCa6+42ZGWmqqmcnuWReYMnkGbNfzCQMvTzJ15/k1M9P8siZ7RdmMuXxCTP7bkzyY1X1Q0n2JblpBfX+fpLfn9n1siRf1t1/nuRfzDnkI0m+s7tvr6rPzl9Ny0ySVNVTklyX5LmZBNRfqKp7uvvnl5xnZ5Lv6O4jp6oRgO1FWANgTVXVr3T3P0jy8SQfm9P+OUn2dPfXTrcPVNXfPskp9yT560v2nTe70d23Thco2Zfk97r7N878Ozhjn5/ked39iSSpqm9OcuXSTt39pqp6SlX98+5++cz+tyd5+7pVC8BwhDUA1tqO5FPTGE/Q3X9SVV83s/2qZNnVIJPkkd39Zae6aHffmuTWlRZZVb+U5OIl+2aP/7Pu/pol/V4zW+e0/59199d0988tqef+JEsXWjnuITnFc20AbD/CGgBr7fPnrAaZTEadPpRMVgM5jfM9bkmIOu5buvv9c/avSHf/w1P3Wnm/M/BN09cXzPrD7v62OX0B2Abq9P5+BAAAYD2sZHUsAAAA1pmwBgAAMCBhDQAAYEDCGgAAwICENQAAgAEJawAAAAP6/wFC0OSUQesOlQAAAABJRU5ErkJggg==\n",
      "text/plain": [
       "<Figure size 1080x720 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "sns.set_palette(\"Set1\")\n",
    "plt.figure(figsize=(15, 10))\n",
    "\n",
    "sns.histplot(x3, bins= np.arange(100), color='yellow', alpha = 0.2)\n",
    "\n",
    "plt.axvspan(xmin = 38.5, xmax = 100, alpha = 0.2, color = 'red')\n",
    "plt.axvspan(xmin = -13.5, xmax = 0, alpha = 0.2, color = 'red')\n",
    "\n",
    "plt.ylabel(\"\"); plt.title('수학 문제풀이 소요시간 IQR 구간')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 165,
   "id": "0a5a1774",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\shk97\\anaconda3\\lib\\site-packages\\seaborn\\distributions.py:1657: FutureWarning: The `bw` parameter is deprecated in favor of `bw_method` and `bw_adjust`. Using 0.1 for `bw_method`, but please see the docs for the new parameters and update your code.\n",
      "  warnings.warn(msg, FutureWarning)\n",
      "C:\\Users\\shk97\\anaconda3\\lib\\site-packages\\seaborn\\distributions.py:1657: FutureWarning: The `bw` parameter is deprecated in favor of `bw_method` and `bw_adjust`. Using 0.1 for `bw_method`, but please see the docs for the new parameters and update your code.\n",
      "  warnings.warn(msg, FutureWarning)\n",
      "C:\\Users\\shk97\\anaconda3\\lib\\site-packages\\seaborn\\distributions.py:1657: FutureWarning: The `bw` parameter is deprecated in favor of `bw_method` and `bw_adjust`. Using 0.1 for `bw_method`, but please see the docs for the new parameters and update your code.\n",
      "  warnings.warn(msg, FutureWarning)\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "<matplotlib.legend.Legend at 0x244a2b6d9d0>"
      ]
     },
     "execution_count": 165,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAA3oAAAJLCAYAAACxAuTEAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjUuMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8qNh9FAAAACXBIWXMAAAsTAAALEwEAmpwYAAB2+UlEQVR4nO39eZikd13v/z8/d229L7NnXwghhC2QAAmQEAKEgCwiiIAbbmjUcyFHDxxXvgiICB79eTwqoKgHNCwHCKtIAIEQIBrWBMieTGYmySw903vt9fn9cVfP9Ow9PV3dtTwf19VXd911113vmeqa6Ve/P0uIMSJJkiRJ6h7JWhcgSZIkSVpZBj1JkiRJ6jIGPUmSJEnqMgY9SZIkSeoyBj1JkiRJ6jLZtS5guTZs2BDPPvvstS7jcHNzUK+vdRWQycDg4FpX0dna5bWUJEnSyumin5O/9a1v7YkxbjzSfR0b9M4++2xuueWWtS7jcJ/7HGw84t/16tq9G665Zq2r6Gzt8lpKkiRp5XTRz8khhK1Hu8+hm5IkSZLUZQx6kiRJktRlDHqSJEmS1GU6do6eJAmqwPYkoRQChLDW5UirI0b6YuT0RoPcWtciSW3KoCdJHWx7kjC8aRNnj44SDHrqETFGJqam2L5rF+c0GmtdjiS1JYduSlIHK4XAekOeekxoft+X/L6XpKMy6ElSJwvBkKeeFByuLEnHZNCTJK2I57/0pQfdfs4LX7hGlbSn6elpdjz44DHPuf2OO7jzrrtWqaL286rXvOag27947bVrU4gkdQHn6ElSFznzgn62bV+53+GdcXqDB24vHvX+//rWt3j3+94HwHe//31++Td+A4D/8brXHXbuT7zqVezdt++gY3fcdRcP3XPPitV7mAsugO3bV+56p58Ot99+zFNmZmb4tde9jp27dvHA9u0MDw0xPjbGvslJXvqiF/EHb3wjMzMzvPa//Td27trFuvFx/uFv/obR0VG++V//RTab5fxHPnLlal7kzHdfwLaZlfv7OGP4dB741WP/fSz2nve9j1qtxq+/9rX7j9140028+e1vB+A73//+/l8Q/Pnb384D27atWK2S1GsMepLURbZtT/iPzx49mJ2oZ72g/5j3P+4xj+Gtf/RH3HHnnTzl4ot57IUXcu4557BufPywcz923XWHHfuxl71sxWo9ou3b4bOfXbnrveAFxz3lrX/2Z7zy5S/nRS94AeVymWdecw1/+Y53sGdigq994xsAvON//S9e9pKX8PKXvpTPfO5zvOUd7+Bdf/InK1fnUWyb2c5/vGLl/j6e9eHj/30suPuee/jMv/87MUaufvazOe8RjwDg8qc/nX//xCe4/lOf4u577+WC88/nRS94AUnioCNJOhn+KypJWra+vj7+38c/zr986EP09/fz1+9+N1/6ylfI5/NLenwmk2lxhavv/q1bedYVVwBQKBR4+qWXkssdvAnAt777XV724z8OwI9dcw23/fCHlEolqtXqapfbctd9+MNc+7rX8Q//9//ygb//e97/3vfyt3//9/zCr/0a//DP/wzAb73hDUzPzPDCa67h4Z07eeMf/iEA9XqdK6+5hk9+5jNr+UeQpI5kR0+SdFI+/bnP8bnrrwfg1a94BS9+xSt49SteQaPR4DkvfCGv+/Vf58//6q+O+vgrr7mG//nbv801z33uKlXcWj//0z/Nm972Nv7Hb/0W99x7L1+/+Wa+d+ut+4duLli8iM6+yUl+7XWv4+577+XXfumX1qLslnnKJZfw0he/mL6+vv3H/vztb2d+fp7tO3YAcOfdd/O2N72JkZERTtmyhZ/9lV8B0l8EfOHTn16TuiWp0xn0JEkn5cILLuDv/v7vufLyy7n+05/m6ZdeCkCSJPt/SH/RC17Al778ZeaLBw8rzefzXP3sZ696za30guc9j9NPO41/+dCH2LhhA1/6zGfo7+/nxptu4hv/+Z8A9BUKTE9PMzIyQrFYZN34OP/07nfzTx/4wBpXv7K++B//wdv//M+Pec4bXv96/uANb+DFr3gF+XyeWq3Gn/7xH69ShZLUvQx6kqST8s63vY0PffSj/OuHP8xFj388L33xi5f82De97W1dF/QAHv/Yx/LVr32N9193HR/44AdpNBpc9PjH88d/8AcA/Mov/AK//Xu/xxtf/3r+f3/zN/z8q1+9xhW3xrOf9Sye/axn7b/9gQ9+kFqtxmt+5mcOO/fLn/vcYcfe9qY3tbQ+SepmBj1J0knJZDLcceed/HFzXtWCz3/ykwfd/pv3vpfpmRnCor3/ZmZmVq3O1fThj36Uu++9l3/7+MfJZtP/aj/wwQ/yu296E/+/d76TFzzvefQVCrzv/e/nBc97Hs+/+uo1rnht3b916/4VWxf7wY9+1NpVWSWpixn0JKmLnHF647grZZ7o9Zbi5ltuOezYoasmzs7NHRb+Wu7005e0UuYJXW8JiqUSI8PD+0MewLrxcYqLhq5edeWVXHXllStX2xKcMXz6Ca2UuZTrrYSzzzrriHPxrmkuWCNJOnEGPUnqIsfa866VSqXSETdIf+fb3sYTn/AEALZt337Ec979V3/FI849tzWFHWfPu1b52Ve9ij9++9u58ppryOfz1Ot1zjj9dP7iT/90TepZcCJ73rXC5k2bqNfra1qDJPUKg54k6aQdaX7VoX5whK5ft0qShP/v93//hB93pLlr3eS5V111Que7KIskLZ/76EmSpLZ00eMfv9YlSFLHMuhJUieLkRjjWlchrboYI/i9L0lHZdCTpA7WFyMTU1OGPfWU2Py+7/P7XpKOyjl6ktTBTm802L5rF7t374bmlgVS14uRvhg5vbG0VWElqRcZ9CSpg+WAc/xhV5IkHcKhm5IkSZLUZQx6OqL//E9461vXugpJkiRJy2HQ0xG9612whG2xJEmSJLUhg54Os3cvfOITMDm51pVIkiRJWg6Dng7zL/8Cj3oU7Nu31pVIkiRJWg6Dng7z3vfCy18OU1NrXYkkSZKk5TDo6SDf+Q5MTMDTnw6lElSra12RJEmSpBNl0NNB3vteeN7zIJOB4WHn6UmSJEmdyKCn/Uol+OAH4eqr09sjI87TkyRJkjqRQU/7ffzjcP75sGVLent42KAnSZIkdSKDnvZ7z3sOdPPAoCdJkiR1KoOeAKhU4Kab4BnPOHBsaMigJ0mSJHUig54AKBahUIB8/sCxwUGDniRJktSJDHoCDgS9xQx6kiRJUmcy6AlIV9w8NOgNDaV76kmSJEnqLAY9AUcOesPDsHfv2tQjSZIkafkMegLSoZuL5+eBQU+SJEnqVAY9AUcfuukcPUmSJKnzGPQEpEHvSB09g54kSZLUeQx6Ao4e9CYn16QcSZIkSSfBoCcgnaOXyx18bHgYpqbWph5JkiRJy2fQE3DkOXoDA2kArNXWpiZJkiRJy2PQE5AGvUM7ekmSLsji8E1JkiSpsxj0BBx56CbAyIgLskiSJEmdxqAn4MiLsYArb0qSJEmdyKAn4NhBz6GbkiRJUmcx6Ak4+tBNN02XJEmSOo9BTwDMzx+5o2fQkyRJkjqPQU/AkbdXABgcNOhJkiRJncagJyAdunm0jt7ExOrXI0mSJGn5DHoCjh309u5d/XokSZIkLZ9BT8DRg97wsEFPkiRJ6jQGPQHuoydJkiR1E4OegGMP3TToSZIkSZ3FoCfADdMlSZKkbmLQE3D07RWGh2FqavXrkSRJkrR8Bj0BUC4fuaM3OAhzc1Cvr35NkiRJkpbHoCfg6HP0kiQNe3b1JEmSpM5h0BOQdvSONHQTYGTEBVkkSZKkTmLQE3D0oZvgFguSJElSpzHoCTj6qptg0JMkSZI6jUFPxAiVysFB7+7Z7zJZ2Q24l54kSZLUaQx6olyGXA5CSG/XY50//MFL+eqejwIGPUmSJKnTGPR02B5635j4FA+X7mei/CCQrrpp0JMkSZI6h0FPFIsHB70Pb/tzHjH4eHZXdgBpR2/v3jUqTpIkSdIJM+jpoI7eXTPfYUfxbp6x4SfYW3kISIPexMQaFihJkiTphBj0dNCKmx/a/i6etuHFjOc2MlFOg97wsB09SZIkqZMY9LR/6OZE+SG+MfFpLlv3QkZy69lb3Qm4vYIkSZLUaVoW9EIIbwkhfCWEcFMI4TGLjg+FEK4LIXw1hHB9CGGkeXxTCOHjIYSvhxA+2Kq6dLiFjt7HdvxvnjT+bAaywwxnx5mq7qERGwY9SZIkqcO0JOiFEC4HNscYnwn8KvDORXe/HvhUjPEK4Abg2ubxdwB/GGN8Wozxla2oS0e2EPQ+v/P/8rT1LwIgm+TpTwaZrk4wNASTk2tboyRJkqSla1VH72rgOoAY423AukX3XQV8pPn1R4HLQgjjwHrgD0IIN4YQfvZIFw0hvDaEcEsI4Zbdu3e3qPTeUyymQW+yupsN+dP2Hx/NbWCi8hDDwzA1tYYFSpIkSTohrQp6m4DFSawWQlh4rkKMsdr8egIYB84Fzgd+gzQk/loI4ZRDLxpjfE+M8ZIY4yUbN25sUem9p1SCTF8JgFyS3398OLeOvZWHGRyE2VloNNaqQkmSJEknolVBb4o0wC1oxBgXYkJjUegbJw2ENeDmGONEjLEIfA04r0W16RClEiT9U/Rnhg46Ppxdx0TlITIZGBiwqydJkiR1ilYFvRuBlwOEEC4Eti+672bgJc2vXwZ8AbgTeExzoZYMcEnzmFZBqQShb5KBzPBBx4ezY/v30hsZcUEWSZIkqVO0Kuh9BsiHEG4E3gW8MYTwjhBCHng78NoQwpeBi4F/bHbx3gp8Efgq8M8xxp0tqk2HKBYhFo7Q0cuNM1F5MP3alTclSZKkjpFtxUWbwzSvPeTwG5uf9wDPP8Jjrgeub0U9OrZSCeg7POiNZNezdf5HgEFPkiRJ6iRumC5KJWjkJunLDB50fCS33o6eJEmS1IEMemJ+Hhr5KfqSgYOOj2TXsbeSjqAdHDToSZIkSZ3CoCeKRajnJilkDg56w7l17GsGvYEBmJ5ei+okSZIknSiDniiV0qB3aEevLxmkQZ1ifZb+frdXkCRJkjqFQU8Ui1DNTB62GEsIgdHcxv2bphv0JEmSpM5g0BPz81DJ7DtsMRZI5+lNlB9icBAmJ1e/NkmSJEknzqAnSqUjd/RgYeXNhxgYsKMnSZIkdQqDniiVoByOHPSGs+P7h266GIskSZLUGQx6oliESpiiLzl86OZQdoyJyoOuuilJkiR1EIOe0o4e00ceupldx57yDgYHYWZmDYqTJEmSdMIMeqJUglKcPvJiLM05eg7dlCRJkjqHQU8USw1KceaIQW84u27/HD07epIkSVJnMOiJYn2WfOgnEzKH3TeSW8/eysP09TU3Vq+vQYGSJEmSTohBT5SYou8I8/MAhrKjzNWnqMeqXT1JkiSpQxj0RJkpBjLDR7wvCRmGsuPsq+5iaMh5epIkSVInMOipuYfe4fPzFoxm17O38hBDQ26aLkmSJHUCg16PazSglp2iP3v0oLcwT8+99CRJkqTOYNDrceUyZAenjriH3oLh7Dq3WJAkSZI6iEGvxxWLkB2apJAMHPWcoewoE+UH7ehJkiRJHcKg1+NKJcgMTB1xD70FI7l17CnvoL/foCdJkiR1AoNejyuVIAzso+8YHb3BzCiTtT0MDLgYiyRJktQJDHo9rlSC0L/vmKtu9mWGmK9N099v0JMkSZI6gUGvxxWLQN/kMRdj6csMMFebYnDQoCdJkiR1AoNejyuVIPZNHnOOXl9mkPn6jEM3JUmSpA5h0OtxpRLE/LG3V+hLBpmrT9vRkyRJkjqEQa/HFYtQzx171c3+zCDF2oxBT5IkSeoQBr0eVypBIzdNf3L0jl4+6afUmKevv+72CpIkSVIHMOj1uFIJapnpYw7dTEJCX2aAzMAsMzOrWJwkSZKkZTHo9biZ+SoxKZNP+o55Xn8yBIUpg54kSZLUAQx6PW6qOE22MUwI4Zjn9WeGiPlpg54kSZLUAQx6PW6yNEW2cfRhmwv6MgPUs1OUSlCvr0JhkiRJkpbNoNfjpsqT5OJSgt4Q8/VpBgawqydJkiS1OYNej5sqT5FfQtArJAPM1acYGsKVNyVJkqQ2Z9DrcdOVSXLh6HvoLejLDDBXSzdNN+hJkiRJ7c2g1+Nmq1MUOH7QKyT9zNWnGBgw6EmSJEntzqDX4+bqU+STgeOel3b00qGbU1OrUJgkSZKkZTPo9bj5+iSFJQS9QjLAbG3Sjp4kSZLUAQx6PW4+7qMvOf7Qzf7MEHO1Kfr7DXqSJElSuzPo9bhS2EdfZgmLsTQ7egY9SZIkqf0Z9HpcJUwykFnKPnqDzDX30XOOniRJktTeDHo9rpJMMZBbYtCrTTE4CJOTra9LkiRJ0vIZ9HpcNTvJQHYp++gNMl+fsaMnSZIkdQCDXo+rZ6YZXEpHLxlkvp5umG7QkyRJktqbQa/HNXLTDOWX2NGrzbi9giRJktQBDHo9LMZIIzfN4BKCXi7kaVCnMFAx6EmSJEltzqDXw0q1EsSE/nz+uOeGEOjPDJH0Txv0JEmSpDZn0Othk6VJqAyTzS7t/P5kiFiYYmampWVJkiRJOkkGvR62d34KykNLD3qZIchPG/QkSZKkNmfQ62H75mYJtQFCWNr5fZkBqpkpikWo11tbmyRJkqTlM+j1sKm5EiEef37egr7MIMXGNAMDMDvbwsIkSZIknRSDXg+bni+SNApLPr+QDDBXn2J42L30JEmSpHZm0Oth08UiyQl09AqZAeZq6abprrwpSZIktS+DXg+bKZXIcAJBLxlgrjblpumSJElSmzPo9bDZ0ol19PqaQzft6EmSJEntzaDXw2ZLxRPq6PVlBpit7rOjJ0mSJLU5g14PmysXyYSlB73+zCBz9XTVTRdjkSRJktqXQa+HzVVKZE9ojt4gc7Up+vvt6EmSJEntzKDXw+Yr82RCbsnn92cGma1P2dGTJEmS2pxBr4fNVefJnsDQzb7MIPM1h25KkiRJ7c6g18OK1RJZlr5hel8yyLxz9CRJkqS2Z9DrYcXaPLlwAkEvM8B8fYbBQZicbF1dkiRJkk6OQa+HlWpFssmJDd0s1mcZGIguxiJJkiS1MYNeDys3iuRPIOhlQpZMyJIfLBr0JEmSpDZm0Oth5XqRXLL0oZsA/ZlhKEwxM9OioiRJkiSdNINeD6s0iuQzJxj0kkFC37RBT5IkSWpjBr0eVokl8pmlD92EdJ5ePTfl0E1JkiSpjRn0elg1FimcYEevLzNIPTtNsQj1eosKkyRJknRSDHo9rEaJfPYEO3rJIPONKQYGYHa2RYVJkiRJOikGvR5WC0X6TzToZQaYr08zNOSm6ZIkSVK7Muj1sEYoU8ie2NDNQtLPXG2KoSGcpydJkiS1qWyrLhxCeAtwRfM5Xhtj/EHz+BDwXuA0YC/wczHG6RDC9cBmoAz8Z4zxDa2qTal6KJ140MsMMFdLO3qTk62pS5IkSdLJaUlHL4RwObA5xvhM4FeBdy66+/XAp2KMVwA3ANcuuu+FMcYrDXmro5EsY9XNZIDZ2j4GBw16kiRJUrtq1dDNq4HrAGKMtwHrFt13FfCR5tcfBS5rft0AJo910RDCa0MIt4QQbtm9e/eKFtxrao0aAIXciTV1+zKDzNanGBx0jp4kSZLUrloV9DYBi5NYLYSw8FyFGGO1+fUEMN78ehr4YgjhhhDCM4900Rjje2KMl8QYL9m4cWNLCu8VxWqR0Ogjkzmxx6UdvUkGBuzoSZIkSe2qVXP0pjgQ4AAaMcbGwtchhKR5e5xmIIwxvgYghHAq8Dng8S2qTUCxViTU8yce9DJDzNem7ehJkiRJbaxVHb0bgZcDhBAuBLYvuu9m4CXNr18GfKF53kLonAaqqKVKtRKhvoyOXmaAuVo6dHPv3tbUJkmSJOnktKqj9xngBSGEG4EZ4FdDCO8A/hB4O/D+EMLrgLuB32g+5pMhhAEgA/xei+pSU7FahFphGUFvkPn6jIuxSJIkSW2sJUGvOSzz2kMOv7H5eQ/w/CM85gWtqEVHVqwVoZ4ne4LfAX3JIHPNDdMfeKA1tUmSJEk6OW6Y3qNKtRKxViA5we+A/swgxdoMQ0Owb19rapMkSZJ0cgx6PWph6OaJdvTyST+lxjwDgw0XY5EkSZLalEGvRxVrReIyVt1MQkIh6Sc7MGvQkyRJktqUQa9HzVeLxOqJBz2A/swQSf8009MrX5ckSZKkk2fQ61Fz5RLU8yc8Rw/SoBfzU3b0JEmSpDZl0OtRc+UiSSws67F9mUGqmWkaDSiXV7gwSZIkSSfNoNejZktFQswt67F9yQDz9WmGh7GrJ0mSJLUhg16PmiuXSGJ+WY8tZNKgNzTkpumSJElSOzLo9ai5SnHZQa8vGWCuZkdPkiRJalcGvR41W54nw/KGbuaTfubr0wwO2tGTJEmS2pFBr0fNV05mMZYB5mpTDA3Z0ZMkSZLakUGvR81X58mw/KA3W5tkYMCOniRJktSODHo9ar5aJLPsOXqDzNWmGBiwoydJkiS1I4NejyrWSmRY/qqbs/UpBgdh374VLkySJEnSSTPo9ahidZ7scoduJoPM16YNepIkSVKbMuj1qFKtuOyOXn9mcP9iLM7RkyRJktqPQa9HlepFsmF5Hb10w/QZO3qSJElSmzLo9ahyvbTsoNeXDDJfn3Z7BUmSJKlNGfR6VKVRIhuWuepmZoD5+qxBT5IkSWpTBr0eVW4Ulx30Ckk/pfocA4MNg54kSZLUhgx6ParaKJNb5tDNJGQoJP1kB+aYnl7hwiRJkiSdNINej6rE5e+jB9CfGaKRm2J2FhqNFSxMkiRJ0kkz6PWoWiyRS5bX0QPoywxSitMMDMDMzAoWJkmSJOmkGfR6UIyRGhVyycl09NKVN4eH3UtPkiRJajcGvR5UqpXIkiebCcu+RiEZYK7mFguSJElSOzLo9aBirUiGAklm+dfoyxzYS8+OniRJktReDHo9qFQrkYkFMicR9ApJP3O1aQYH7ehJkiRJ7cag14OK1SKZ2Ef2pDp6A8zVp+zoSZIkSW3IoNeDirUiScyfVEcvnwwwX0tX3TToSZIkSe3FoNeDitUiyUkO3exLBpitTTIw4NBNSZIkqd0Y9HpQqVYiaZxk0MsMMFufYnAQ9u5dudokSZIknTyDXg8q1oqERp5sdvnX6EsGmKs5R0+SJElqRwa9HlSsFqF+cnP0+jJDzNXSjt6+fStXmyRJkqSTZ9DrQaVaibACQzfn6m6YLkmSJLUjg14PKtaKUM+d5NDNQeZrMw7dlCRJktqQQa8HrczQzQGKdTdMlyRJktqRQa8HlWolqJ1s0Btkvj7L0BBMT69cbZIkSZJOnkGvBxVrRWIjd1JBr5D0U6rPMTgYDXqSJElSmzHo9aD56jzxJDt6SciQT/qoZ2YBKJVWqDhJkiRJJ82g14OKtSKxenKrbkI6fHOuPs3wsAuySJIkSe3EoNeDitXiSXf0APozQ8zX0qDngiySJElS+zDo9aD56jyNWuGktlcA6EsO7KVnR0+SJElqHwa9HlSsFomVk+/o9WUGma+lWywY9CRJkqT2YdDrQcVakcaKzdGbYmjIoZuSJElSOzHo9aBirUi9evIdvULSz1xtmoEBO3qSJElSOzHo9aB06ObJz9ErJAPM19Ohm3b0JEmSpPZh0OtBpVqJWvnkh24WMgc6evv2rUxtkiRJkk6eQa8HlWqlFRm6ma66Oemqm5IkSVKbMej1oGJtZVbdLGQGmK2li7HY0ZMkSZLah0GvB5WqJZJYIISTu05/MshcbYrBQYOeJEmS1E4Mej2oWCuRIX/S1+nLpEHP7RUkSZKk9mLQ60GlWolsKJz0dQqZAeZcdVOSJElqOwa9HlSpl1ck6PUlg8zXZlyMRZIkSWozBr0eU61XAcgmJ7kSC9CXSffRGx62oydJkiS1E4NejynWiuSTPjInuVk6NDt69Rn6+6FSgWr15K8pSZIk6eQZ9HpMsVoknymQPfmGHn2ZAYr1WSAyPOzKm5IkSVK7MOj1mFKtRC4UTnoPPYAkZMgnfZQac4yMGPQkSZKkdmHQ6zHFWpFcsjJBD6A/M8hcbdqOniRJktRGDHo9plgtkgsFsiswRw+gLzPEXG3KoCdJkiS1EYNej0n30MuvWEdvIDPEXH2KwUG3WJAkSZLaxQr1ddQpirUiWQqswO4KAPRnhpmu7mVoyI6eJEmS1C4Mej2mWC2SIb+CQW+ImdpeBgcNepIkSVK7MOj1mFKtRIb8iuyjBzCQGWamto+hIZiYWJlrSpIkSTo5ztHrMcVakYSVm6PXlxlkprqX4WHYu3dlrilJkiTp5Bj0ekyxWiQTCyQr9MoPZIaZqu5haMigJ0mSJLULg16PKdVKJDG/YtsrDDQXY3F7BUmSJKl9GPR6TLFWJMTcCm6YPsx0bcKgJ0mSJLURg16PKdfK0Miu3NDN7IHFWKamVuaakiRJkk6OQa/HlGolQmPlOnqDmRFmavsYHjboSZIkSe3CoNdjSvWVDXr9mWFma/sYGID5eajXV+a6kiRJkpavZUEvhPCWEMJXQgg3hRAes+j4UAjhuhDCV0MI14cQRg553P8KIfxpq+rqdenQzZULegOZIWZrU4QQGRqCycmVua4kSZKk5WtJ0AshXA5sjjE+E/hV4J2L7n498KkY4xXADcC1ix53JvDcVtSkVKlWItbzKzZHL5vkyYYspcYcIyMuyCJJkiS1g1Z19K4GrgOIMd4GrFt031XAR5pffxS4bNF9fwK8o0U1CSjXy1DPrdj2CgCDmVG3WJAkSZLaSKuC3iZg96LbtRDCwnMVYozV5tcTwDhACOGXgG8B24920RDCa0MIt4QQbtm9e/fRTtMxlGolqK3c0E2AgeyBBVkMepIkSdLaa1XQm6IZ4JoaMcbGwteLQt84sDuEcD7wUuAvj3XRGON7YoyXxBgv2bhx40rX3BPKtTKN+goHvcwwM9W9DA0Z9CRJkqR20KqgdyPwcoAQwoUc3KW7GXhJ8+uXAV8AXt2s5Trgj4AXhxBe2qLaelq5XibW8ise9KZrexkcNOhJkiRJ7WAFZ2od5DPAC0IINwIzwK+GEN4B/CHwduD9IYTXAXcDvxFjLC88MIRwJXBNjPHjLaqtp5VrZeIKz9Fb2GJhcNBVNyVJkqR20JKg1xymee0hh9/Y/LwHeP4xHvtl4MutqEtpR69RXdmhm32ZQaabQzf37l2560qSJElaHjdM7zGlWom4wkFvIDPETC0NehMTK3ddSZIkSctj0OsxlVqFxgrP0evPDDNV3cPwsB09SZIkqR0Y9HpMuV6mvuLbKwwzXZ1wewVJkiSpTRj0eky5XqZRWemhm+6jJ0mSJLUTg16PqdQr1Fs4R89VNyVJkqS1Z9DrMeVamVjNr+j2Cos7elNTK3ddSZIkSctj0OsxlXqF2koP3cwOM1ubYnAQZmag0Vi5a0uSJEk6cQa9HtOKoZuFZIByfR6SGgMDMD29cteWJEmSdOIMej2k3qhTj3Xq1eyKBr0kJM2u3iQjIy7IIkmSJK01g14PKdfLFDIFatWwonP0IJ2nN13da9CTJEmS2oBBr4eUa2XymTy1Oiva0QMYzIzsX3nToCdJkiStLYNeDynXm0GvuvJBbyA7wkzVvfQkSZKkdmDQ6yELHb16nRUfutmfGWLajp4kSZLUFgx6PaRcL5PL5KjWVr6j19/cNH1w0KAnSZIkrTWDXg8p18rkkzz1VgW96j6DniRJktQGDHo9ZKGj12hAssKvfDp0cw9DQzAxsbLXliRJknRiDHo9pFwrkw05slkIYWWvPZAZZqoy4WIskiRJUhsw6PWQcr1MNsmv+LBNSPfRm6ntZXgY9u5d+etLkiRJWjqDXg9Z3NE7TLVyUtceyAy76qYkSZLUJgx6PaRcL5MJOTKHBL2Be2/lwre+mszs1LKvPZAdZrY2yfAwTE6eXJ2SJEmSTo5Br4eUa2Uy5MgeMnSzf8fdZOZnOPO6P4UYl3Xt/swwM7V9Bj1JkiSpDSwp6IUQ3h5COL3Vxai1yvUyCbnD5uj17XqAfZc8l/yeHay/6RPLuvZAJu3oDQ5GpqeXnRclSZIkrYCldvS+ALwzhPCvIYQrWlmQWmd/R++QoZuFnQ9QWX8Ku57z05zy2fdReOi+E752LsmTDVlqyTyFAszMrFDRkiRJkk7YkoJejPGLMcZXAa8HfjmE8J0Qws+HsNKL9KuV0o5e9vCO3u5tVMY2UR3fzJ7Lfoyz/++bCctYnGUgM8JMdS8jIw7flCRJktbSUoduDoQQfgH4B+Bh4KeBzcD7W1ibVli5VibEgzt6oVImO7OP2vA6AGYveAr1gVHWf/2TJ3z9wewI080tFlx5U5IkSVo7R1po/0i+BLwPeEWMcb557IchhI+0piy1wsIcvWRRvC9MPEh1dAP723whMHfWBQxsu+OErz+QGWG2uSCLQU+SJElaO0udo/ehGON7FkJeCOFagBjjT7asMq24cq1MErMHdfQKux6gOr75oPOqY5vpe3jrCV+/PzPEdNWOniRJkrTWjtnRCyGcCjwO+PkQwg+ah/uA1wF/2+LatMJKtRIhHrzqZmHXNioj6w46rzK+icLubenSmScwDXMgM8yMm6ZLkiRJa+54Qzf7gEuBUeCy5rE68IutLEqtUaqXSA4Jen07t1Id23jQeY3+IWImR3Z6gtrohiVfvy8zxHR1gsFBg54kSZK0lo4Z9GKM9wJvDiH8V4zxs6tUk1qkXCtDo0DmkKGb82c++rBzK+u30PfwVmZPIOgNZUfZV93J0CDs3bsSFUuSJElajuMN3Xx1jPFfgctDCM9YfF+M8fdaWplWXKlWImkMH+joxUhh9w4q45sOO7cytom+XQ8w+6iLl3z94ew4D5e2csqwQU+SJElaS8cburkwL+9zrS5ErZd29A4M3czMTRGARt/gYedWxzae8MbpQ9lx9lVvZnQUfvSjFShYkiRJ0rIcc9XNGOP3ml/eE2P8CvBVYAi4rdWFaeWV6qU06DVf9b5d6UbpR1pwpTK+mf6d95/Q9Yez4+yr7GJ0FHbvXoGCJUmSJC3LUrdX+HDz868BTwH+qSXVqKXKtTLJoo5eYdc2KuMbj3huZXwzhV3bTuj6w7lx9lV3MTICe/acbLWSJEmSlmupQa/R/PzoGOObgMPH+qntletlYj2/KOg9QHXkyIut1IfGSColMsXZJV9/KDuWbpg+0nCOniRJkrSGlhr0bgghfAf4UAihDyi0sCa1SLlWhnqOZGHo5s6tVI/S0SMEKuu2UDiBjdMzIUt/ZggGJti7N92GT5IkSdLqW1LQizG+Ocb4xBjjTTHGUozx6a0uTCsv7ejlyDaX4Cns2kZ19PAVNxdUxjbSt3PpQQ9gOLuOYrKTJIH5+ZOpVpIkSdJyHW/VTQBCCE8DXg+sIw2HMcZ4VSsL08pbWHUzSYB6nfy+nVSOsU9edWwjhYfvP6HnGM6uY29lJ2Njj2XPHhh0kK8kSZK06pYU9IB3Az8H/AhwQF6HqtQrNKp5slnI732Y2tAY5PJHPb86voWBe289oecYzo6xr7KT0dF0QZazzjrJoiVJkiSdsKUGvW0xxu+0tBK1XLleplHNkU3ShVgqY0cftglQGd/Eut0PnNBzDGXHmKzu2h/0JEmSJK2+pQa920IIbyPdRy8CxBg/37Kq1BLlWplYS+fo9e3aRnXs6MM2AaojG8hN7SVUK8RjdP4WG8yOsrfyMKOjMDGxElVLkiRJOlFLXXVzDqgAlwKXNT+rw6RDN9N99Aq7tlI7xvw8ADIZqqMbTmg/veHsOBOVhxgasqMnSZIkrZUldfRijG8OIeSBzTHGE9tFW22jUq9Qr+XJ9EPfzgeYetwzjv+YdZsp7NxK6bRHLOk5hrLj3DP3fU4dgd27T7ZiSZIkScuxpI5eCOHngc8Cnw4h9IUQ3tzastQKizt6+T07qIwdZQ+9RaqjG+k/gS0WhnPj7KvsZGQEdu06mWolSZIkLddSh27+cozxOcDeGGMJeGoLa1ILxBjTjl41RyYTyc5NUR8YPe7jKus2ndAWC8PZcaaqu12MRZIkSVpDSw16MYSQ4cDWCsdPCGor1UaVTJKhXk3oa8wTs3nIZI77uMrY5hPaNH0oO85UdYKRkWjQkyRJktbIUoPeO4HPA+eFED4F/EPrSlIrlGtl8pk81RoM1Gao9w0s6XHVsU0U9jwI9fqSzs8nBTIhS35kylU3JUmSpDWy1MVYPhVC+CpwPnBfjNFeTYcp1Urkkzz1GvTXZqj3DS7pcTFfoDY0Qn7vw1Q2nrakx4zk1hMHdjIxMXYSFUuSJElaruN29EIIl4UQ3g1cB/wsMNzyqrTiyvUyuUyOahX6qtM0Cv1Lfmx1dCP5PTuWfP5Idh3Vwk727oUYj3++JEmSpJV1zKAXQngB8Dbg3cDPAB8D/imEcM4q1KYVtDB0s1aDvuosjcLSOnoA1ZH1FCYeXPL5Q9lxZtlJNgtzc8upVpIkSdLJOF5H77eAV8YYvx1j3Btj/DLwi8BbWl2YVla53pyjV4W+yol19GrD4xT2bF/y+YPZUfZVdrnypiRJkrRGjhf0cjHGg3ZDizHeA2xuXUlqhXItHbpZq0OhMkM937fkx1ZH11PYvfShm0PZUfZVHmZszKAnSZIkrYXjBb2jzbBa6mqdahPleplckqNeg0JlmsYSV90EqI5sID/x0JLPH86OM1F5yI6eJEmStEaOt+rmxSGErx9yLACPblE9apH92ytUoVCcorFu6WvqVEfXk9/7cLqySgjHPX84O8724l2MjOAWC5IkSdIaOGbQizG6MXqXWFh1s1aHfHmaWt/SR9/GfD8xmyM7s4/ayLrjnj+UG2dfZSenDdvRkyRJktaCQzB7RLl2YOhmrjRzQkM3AapjS99iYTg7zmR1N8PDsHv3cqqVJEmSdDIMej1i8aqbudIM9cKJBb3KCWyxsBD0Rkdh167jny9JkiRpZRn0esRCR69Wh2xp9oSDXm14HYUldvQKyQCNWKd/dM6OniRJkrQGDHo9YmGOXr2WBr1G39L30YN00/T87qXtpRdCYDS3njC008VYJEmSpDVg0OsR5VqZbJIlVmuEWoWYW/o+egC10Q1L7ugBDGfXEQd2uhiLJEmStAYMej2iXC+TDTmGmKFRGFzSNgmL7d9iYYmGsmPU+3exd++JVipJkiTpZBn0ekS5ViYTsoxnZqj3n9j8PID6wAhJuUhSml/S+UPZcSq5nezdm26/J0mSJGn1GPR6RLleJiHHWGY67eidqBDSLRaWuPLmYHaU6cZOcjmYnT3xp5MkSZK0fAa9HlGqlUjIMZrMUC+c2EIsC2ojGyjsWeoWC2NMlB9ibMxN0yVJkqTVZtDrEaVaiSTmGA0nvofegurIuiV39Iaz4+ytGPQkSZKktWDQ6xHlWpkMOYbDDI1ld/TWUVjiFgvDuXXsrTzM6KhBT5IkSVptBr0eUaqnHb0RZmjklxf0KiMbKOxZWtAbzW1gT+VBRkZwLz1JkiRplRn0ekS5VibEPCNMnfBm6QtqI+sp7HloSeeO5jawr7KToeFoR0+SJElaZQa9HlGupatujsTpZS/GUh1ZR3ZmL9Rrxz03n/SRSwrkRyfYvXtZTydJkiRpmQx6PaJULxEaOYbiNI2+ZWyvAJDJUhsaJb9355JOH89tIhndwa5dy3s6SZIkScvTsqAXQnhLCOErIYSbQgiPWXR8KIRwXQjhqyGE60MII83jfxZC+FII4b9CCFe1qq5eVa6VSWKOocb0slfdBKiObljyypujuQ3E4R129CRJkqRV1pKgF0K4HNgcY3wm8KvAOxfd/XrgUzHGK4AbgGubx98SY7wKeCnwP1tRVy8r18vQyDMYZ5c9Rw+gNryewhKD3khuPdW+HS7GIkmSJK2yVnX0rgauA4gx3gasW3TfVcBHml9/FLised5M89j5wPdbVFfPKtfKhEaOgcYsjZPp6J3IFgvZdZTy2w16kiRJ0irLtui6m4DFA/ZqIYQkxtgACjHGavP4BDAOEEJ4LvAOYBD4sSNdNITwWuC1AGeeeWaLSu9O5XoZQpb++uzJDd0cWc/AtjuWdO5obgMTlW0GPUmSJGmVtaqjN0UzwDU1miEPoBFCWHjecZqBMMZ4Q4zxSaTdwH850kVjjO+JMV4SY7xk48aNLSq9O1VqFZJyg3rIQWb5+T6do7f0LRam4nb27YMYl/2UkiRJkk5Qq4LejcDLAUIIFwKLx/rdDLyk+fXLgC+EELIhhIU20x4g06K6ela5XiY3V6aYWeaKm03V0Y3pYiz1+nHPHc1tYG/1QfJ5mJk57umSJEmSVkirgt5ngHwI4UbgXcAbQwjvCCHkgbcDrw0hfBm4GPhHoAB8unns08DvtqiunlWul8nOV6hklj9sEyDmC9QHR5e08uZYbgMTlQcZG8NN0yVJkqRV1JI5es1hmtcecviNzc97gOcfcl+ZdJEWtUilXiE3X6KcPbmgB1BZt4X+nVupbDrjmOcNZseYr89y+roSe/b0ce65J/3UkiRJkpbADdN7RLlWJj9XopJd/tYKCypjmyg8dN9xz0tCwlhuA/2bHnQvPUmSJGkVGfR6RKVeoVAsUj3JoZsAlXWb6X/o3iWdO5bbSGHDDh5a2votkiRJklaAQa9HVOoVCrPzVDJ9J3+t8S30PXz/ks4dyW0gM27QkyRJklaTQa8H1Bt1GrFBrjhLLXfyQzer45vJ79mxpJU3R7LrCCM72LbtpJ9WkiRJ0hIZ9HpAuV4mn8lTmJ+mmjv5oZsnsvLmSG491YFt7Nhx0k8rSZIkaYkMej2gXEuDXq44TS1/8kEPmitvLmH45lhuI6X8dh48fiaUJEmStEIMej1goaOXL8+sXNAb20TfElbeHM1tYDbZzsMPr8jTSpIkSVoCg14PWOjoFcrT1Aor1dHbTN/DSwt6U40HmZhY0pQ+SZIkSSvAoNcDyvUyuUyOQmWWuGJBb2krb47kNjBZ3cXwSHQvPUmSJGmVGPR6QLlWJp/kKdRmqfetUNAb30Jh9/FX3swnBQpJP+tO3+M8PUmSJGmVGPR6QLleJpdkyTYqxEJhZS6ay1MbGk23WTiOsfxGBrfsMOhJkiRJq8Sg1wPKtTI5EsqZfjKZlXvJK+u20L9z63HPG81tpLDBoCdJkiStFoNeDyjXy+QbCcVkiExm5a5bGd+8pJU3R7LrScbcYkGSJElaLQa9HlCulck1oBT6yWZX7rpp0Lv3uOcN59YRh7ezffvKPbckSZKkozPo9YByvUyuDvNhkGQFX/F0i4X7j3veaG49lf5t7Dj+dD5JkiRJK8Cg1wPKtTK5eoMSK93R20Jhz4PHXXlzNLeB+axDNyVJkqTVYtDrAeV6mVy1wXzsX9E5eunKm2PHXXlzLLeR2fAgDz+8gs8tSZIk6agMej2gVCuRqzWYZ4WDHlBZv4X+4wzfHM1tYLL+IPv2Qa22ss8vSZIk6XAGvR5QrpXJlmvMx5UduglQGdtE38PHXpBlMDNKpVFkdMM8u3at7PNLkiRJOpxBrweU62VylRqzjYEVXYwFoLzpDAbvvfWY54QQGM9vYeSMbc7TkyRJklaBQa8HlGtlcuUa842+Fe/oFU99BIP3/xDqxx6TuS6/mYFTthr0JEmSpFVg0OsB5XqZTKVGMRZWvKPX6B+iOrqB/m13HvO80dxGMuseMOhJkiRJq8Cg1wNKtRK5Uo1K0k8IK3/94qnnMnz3d455zlhuI3HEjp4kSZK0Ggx6PaBUK5GrVKlmCq25/qnnMXTnt495znhuE9XB+9m+vSUlSJIkSVrEoNcDFjp69WxfS65fPOVcBrcee57eWH4z84X72XHsLfckSZIkrQCDXg8o18rkSxVqmdYEvUb/INXRjQw8cMdRzxnPb2ImuOqmJEmStBoMej2gXC2Sr9ZpZPMte47iaecydM/R5+mN5TYxHR/ioYcbLatBkiRJUsqg1wNK5TmySZ4k04KVWJqKpzyC4WPM08snBQYyw0zWdlKttqwMSZIkSRj0ekK5GfSyudY9R+nURzCw9UdQO3qKW5ffwsjpD7BzZ+vqkCRJkmTQ6wnl8jyZJE+mha92o2+AythGBrYdfZ7eWG4Tg6e5xYIkSZLUaga9HlCuFsmGAplsa5+ndOojGDrGfnpjuY3kNrhpuiRJktRqBr0eUKqWSEKBTKa1z1M89VyG7/zWUe8fy2+EsfsNepIkSVKLGfR6QLlWIrMKQa906nnpFgtHmae3sGm6e+lJkiRJrWXQ6wGlepkk9LU86DUK/VTGNzN0761HvH8sv5lSYatBT5IkSWoxg14PKDUqhFUIegCz5z2RdTd/5oj3rctvZjaz3aAnSZIktZhBrwdUGlUC/S1ddXPBzKMuZvQH3yAzP3PYfYOZUWoU2b5rtvWFSJIkST3MoNcDytSA/lXp6DX6h5g7+0LGb/n8YfeFEFiXO4WH5ra1vhBJkiSphxn0ekCZGpGBVQl6ADMXPJX1X/8kxHjYfev6NjOXfYBSaXVqkSRJknqRQa/LxRip0KBBP8kqvdrF084jUy4xsPVHh903ntvEyJlbuf/+1alFkiRJ6kUGvS5XrpfJxUAlrM7QTQBCYOrRT0m7eocYzW2gf8tW7rlnlWqRJEmSepBBr8uVaiUKjUAprs6qmwtmL3gyY7feSFKcO+j4eH4TYd393Hvv6tUiSZIk9RqDXpcr1UoUaoHSKmyYvlh9YIT50x/J2Le/eNDx8dwmaoNbueuu1atFkiRJ6jUGvS5XqpXI1SPFxioO3WyavuCpbDxkUZbx/GaK+Qe4++7VrUWSJEnqJQa9Lpd29CJFCmSzq/vcxTPOJynOMnTP9/YfG8ttZJad3HNffXWLkSRJknqIQa/LlapF8tVIsb66c/QASDJMXvRMNt3w/v2HskmewewoW/c8fKTdFyRJkiStAINelyvPTZNvBCr1zOoHPWDmUZfQ/+B99G8/MClvfX4zhc1befjh1a9HkiRJ6gUGvS5Xmp4gT0KtxpoEPTI5Jp9wBZtu+MD+Q+P5LYye5RYLkiRJUqsY9LpcaWYfeTJUq2sU9IDpCy9l+K5vk9+9HUhX3ixsvtctFiRJkqQWMeh1udLMJHky1OprF/Rivo+pxz6dTV+8DoB1hS3E8btdeVOSJElqEYNelyvNTZIPWeo1yKzyqpuLTT3uGYx/7ytkp/awPn8K5cF7DHqSJElSixj0ulxpbopcyK7dHL2mRv8Q04+6hI1f+Qjr8qcwm73foCdJkiS1iEGvy5WKM+RDlmoNsmsY9ACmHvt01t/8OcbDOLNxJ/c9UF3bgiRJkqQuZdDrcqXiDNlMjnoNkjUOerWxjZTXb2H9j/6L0fx6ptnG7Oza1iRJkiR1I4NelyuVZsklOep1yLTBqz1zwVNY//VPsj5/GuvOu5f77lvriiRJkqTu0wY/+quVSqVZ8pkc1Spk13AxlgWz5zyOgW13sCGOMHTafe6lJ0mSJLWAQa/Llcpz5DJ5anVI2uHVzuWZfeSTOO2hvWQ23uNeepIkSVILtMOP/mqhYmWeXKZAEtZ21c3Fph/9VM69425qw3e58qYkSZLUAga9LlesFclm+tpi2OaCyobT2FQbohG+z113rXU1kiRJUvcx6HW5Ur1MNim0TTdvwdBpl7AvbHUxFkmSJKkFDHpdrlgvk0n6ybRRRw8gOfcySqHK/MP3Uq+vdTWSJElSdzHodblSrJIkfW3X0aMwwJZKPy/Y+B527FjrYiRJkqTuYtDrcqVYJcn0k223oAdsyGzk0aOfcYsFSZIkaYUZ9LpciRohGWi/jh4wNnAG9cE72X7rvrUuRZIkSeoqBr1uVq1SykRC6G+rVTcXrMtu4HunrCf/hc+udSmSJElSVzHodbOZGUr5hKSRa8uO3sawnru3FDjr2x9b61IkSZKkrmLQ62YzM1RygVDLkrThK70hWc+OsQqPfegLUC6vdTmSJElS12jDH/+1YqanKWUDoZ5ry6GbG8I6duf2cFc8h/oNX1rrciRJkqSuYdDrZtPTlLMQatm2HLrZF/roo8BX11/E7P91+KYkSZK0Ugx63Wx6mlImQi3XlkM3ATYm6/n+eWdT+PwnodFY63IkSZKkrtCmP/5rRUxPU05i23b0ADaE9UydVWU+Mwz/+Z9rXY4kSZLUFVoW9EIIbwkhfCWEcFMI4TGLjg+FEK4LIXw1hHB9CGGkefwdIYQvhxBuCSFc06q6ekmcmqKcNIhtHPTWJWNUNjzEbcNPg485fFOSJElaCS0JeiGEy4HNMcZnAr8KvHPR3a8HPhVjvAK4Abi2efwjMcYrgecDb21FXb2mNj1JQiDWMm0b9DaGDcyMbOfL1afB9devdTmSJElSV2hVR+9q4DqAGONtwLpF910FfKT59UeBy5rn3dI8Ng1MtqiunlKa3Uc+JtRqkLRp0NuUbGBP3w5u2nU+cXIS7r57rUuSJEmSOl6rgt4mYPei27UQwsJzFWKM1ebXE8D4wkkhhALwV8CfHOmiIYTXNod23rJ79+4jnaJFSlMT5MlQrdLWHb0HeYihkYT5xzwFPve5tS5JkiRJ6nitCnpTLApwQCPGuLCkYmNR6BunGQhDCOcD/wD8nxjjETdVizG+J8Z4SYzxko0bN7ao9O5RmpmkQLatg95YGGE2zrLh9CLbNl0Mn/rUWpckSZIkdbxWBb0bgZcDhBAuBLYvuu9m4CXNr18GfCGE0A/8L+C1Mcbvt6imnlOemyIfstTq7Rv0kpCwKdlI5swHubVwCXz961AqrXVZkiRJUkdrVdD7DJAPIdwIvAt4Y3NVzTzwduC1IYQvAxcD/wg8DngS8NnmyptfDiGsO8q1tUSluSkKSY5qpX2DHsCmsIHGlh38aPswnHcefPWra12SJEmS1NGyrbhoc5jmtYccfmPz8x7SlTUX+0/g1FbU0stKxRnyIUetDtk2DnobwjqK63dw/xeBZz0JPvMZuPrqtS5LkiRJ6lhumN7FSqVZ8pkctTaeowewMdnAvsFtbN8O9UueAv/2b2tdkiRJktTRDHpdrFSeI5/JU621d9DblGxgR9jByAg8PPRI2LsX7r9/rcuSJEmSOpZBr4uVqkXymXz7d/TCBrY3HmTLFrhvawJPfrJdPUmSJOkkGPS6VYxp0MsW2r6jty6MsS9OMb65wtatwMUXp/P0JEmSJC2LQa9blcuU+rJkkyz1GmRbsuzOysiEDBvCOrJnPMQ995B29L76VSiX17o0SZIkqSMZ9LrV3BylwQL5kKNahaTNX+lNyQYqG3ekU/NGR+Hss+FrX1vjqiRJkqTO1OY//mvZ5ucpDeTIJRnq9fbu6AFsCOuZG9uRrrxZJx2++dnPrnVZkiRJUkcy6HWr+XlK/TlyIUutzefoAWxM1vNg2J6uvPkw8JSnwKc/vdZlSZIkSR3JoNetikXKhSz5Dgl6m8IGtja2c8opcN99wKMelW6zcM89a12aJEmS1HEMet1qfp5iIUMuyVFr88VYIN00fXvjQTZtaga9JIFLL4VPfWqtS5MkSZI6jkGvW83NUSxk0o5evf0XY1kf1rEr7mHjKTXuvrt58KlPhY9/fE3rkiRJkjpRm//4r2Wbm6OUT8iHdHuFdh+6mQtZ1oUxsqftPDBa8+KL4dvfhqmpNa1NkiRJ6jQGvW41N0cxF8iFHPVG+wc9gE3JRubHd7BrV3MLvf5+eMIT4HOfW+vSJEmSpI5i0OtWs7OUcpCJWTIZCGGtCzq+jWEdD4UdbNnSnKcH6eqb11+/lmVJkiRJHceg161mZynmAplGlmwHdPMANiTr2drYzpYtixbbvOyytKNXq61pbZIkSVInMeh1q9lZStlI0si1/YqbCxZvsbB/QZaNG2HLFvj619e0NkmSJKmTGPS61fw8pUzcP3SzE2xMNvBAfTunnroo6EG6+uYnPrFmdUmSJEmdxqDXrebmKCWRpN5JHb2N7Iy72XhKlfvugxibd1x2GXzyk2tamyRJktRJDHrdam6OctIgqWfbfg+9BbmQZUNYx77BHWSzsGtX845HPjLdYuGuu9a0PkmSJKlTdEgE0Ambn6dELZ2jl1vrYpbulGQz9zW2cuqpcO+9zYNJAk97mqtvSpIkSUtk0OtW8/OUQ51Qz5LpoFd5c7KRe+tbD16QBeDyy+Ff/3XN6pIkSZI6SQdFAC1ZtQqNBqVYJannyHTIHD2ALWEzd9fvOzzoXXQR7Njh8E1JkiRpCQx63Wh2Fvr7KTeqhFrnrLoJBw/dPCjoZTJwxRVw3XVrVpskSZLUKQx63WhmZn/Qo57rsKC3iW2NB9mwscHu3VAqLbrzWc+Cf/mXRctxSpIkSToSg143mp2Fvj7KsQLVzuro9YU+hsIguzM72bIF7r9/0Z0XXpj+2b7//bUqT5IkSeoIBr1uNDtLva+PaqwTa5mOWowF4NRk8/4FWe65Z9EdIcCVV7ooiyRJknQcHRYBtCSzs1QH8hRCjnotdFRHD2Bz2MR9ja1s2XLIPD1Ih29ed53DNyVJkqRjMOh1o9lZKv15CkmOWo3OC3rJRu6u38eppx5hkc1HPAKyWfjmN9ekNkmSJKkTGPS60cwM1b5cxwa9U5LN3NtcefO++w5p3jl8U5IkSToug143mp2lUsiSD2nQSzrsVT412cLW+jaGhiK5HOzcecgJV14JH/4w1OtrUZ4kSZLU9josAmhJZmao5tOhm9Vq53X0hsMQgcBE3McZZ8Cddx5ywplnwoYNcMMNa1KfJEmS1O4Met1oZoZyX4Z86MygB2lX777GVk47DW6//QgnPO958Hd/t+p1SZIkSZ3AoNeNZmaoFrLkk2xHztED2JJs4r76Vs44A374wyOc8Oxnw5e+dIRxnZIkSZIMet1odpZKvrM7eunKm/dz5pnpypuNxiEnDA7C5ZfDP//zmtQnSZIktTODXjeamaGay5BLMtRq6W4EneaUsJl7GvcxPAz9/bBjxxFOev7z4T3vcU89SZIk6RAGvW40N0clF/avutmJHb1Tks3c39gGpGuvHHGe3mMek4a8r31tdYuTJEmS2pxBrxvNzVHJZciFbMcO3RwPY8zHeabjDKeddpR5eiHANde4KIskSZJ0CINeN5qbo5INHb0YSxISzk7O5Ie1OzjzTPjRj45y4tVXw6c+BZOTq1meJEmS1NYMet2mXAagGmJHd/QAzs6cyXfrt3H66XDffVCrHeGk0VF4ylPgX/911euTJEmS2pVBr9vMzsLAANVYIx+y1OqdG/QekZzNd2q30t8P69bB/fcf5cRrroG//VsXZZEkSZKaDHrdZmYGBgaoxBq5kKVeg0wHrroJ8IjM2dxW/xH1WOeMM46yIAvAk56U/rm//vVVrU+SJElqVwa9bjM7C/39VBo1ch08Rw9gOAwxGka4t3GMjdMBkgRe+EL4q79a1fokSZKkdmXQ6zbNoFeOVfIhS7WDgx7AuZmz+V7ttmN39CAdvvm5z8FDD61abZIkSVK7Muh1m4WOXqyST3Lp0M1ODnrJmXynfiunnQbbt+9fa+ZwQ0Nw5ZXpBuqSJElSjzPodZvZWejro1yvpnP06pDp4Ff5EZlz+F7tB+RycMopcNddxzj5xS9O99SrVletPkmSJKkddXAE0BE1O3rVWCWfpNsrZDt0MRaAU8JmJuMUexv7jj988xGPSNPg9devVnmSJElSWzLodZuZGejrSxdjIUetnq5V0qmSkPCIzNl8r/4DTjvtGAuyLHjRi1yURZIkST2vgyOAjmgh6DW3V0hCZ8/RAzg7OZPv1m7jrLOO09EDuPxyuOMOuPXWValNkiRJakcGvW4zM9Mculkjqec6etjmgkdkzua79VvZvBkmJ9OPo8pm060W/uIvVqk6SZIkqf0Y9LpNM+hVGjUyMdvx3TyAc5KzuKN+D42kyrnnwm23HecBL3kJfOxjbrUgSZKknmXQ6zazszAwQCXWSBo5Ml3Q0esPfWxJNnF7/S7OOgu+973jPGB0FJ7zHPjLv1yN8iRJkqS2Y9DrNov20Uvq3dHRA3hkci431f6Tc86B739/CQ942cvgve+F6emW1yZJkiS1G4Net2kGvdrCHL0uCXpPzj6Rz1Ru4IwzIvffD6XScR5wyilwySXw7nevRnmSJElSWzHodZu5uf1z9EIt2xWLsQCck5xJjRp3Z+7g9NOXsPomwMtfni7KUqm0vD5JkiSpnRj0ukmMMD/fHLpZo1bOks+vdVErI4TAk7NP5NPVGzjrrCUO3zz/fDjjDPjXf215fZIkSVI7Meh1k3IZQoBsllqjRr2cpVBY66JWzlOzF/Pv1S9x5jl1vvvdJT7oJ38S/vRPodFoZWmSJElSWzHodZPZWRgcBKASa9RLOXK5Na5pBW1ONrIujDNx9re4/Xao15fwoIsvTsPvRz/a8vokSZKkdmHQ6ybNrRUiUI11aqXuGbq54MnZi/hC5vOMjcG99y7hASHAL/8yvOENztWTJElSzzDodZPmZumlRoVcyFAuJWS7qKMH6eqbN1a/wWnnFbn11iU+6OKL01U4/+ZvWlqbJEmS1C4Met2k2dGbb5ToS3IUi1Doso7eSBjmvMw57Hv0TcffOH2xX/kVeOtbYXKyVaVJkiRJbcOg101mZ6Gvj7laib4kT7EIuS4LegBPyT6Jm7d8kltvTRcaXZJzzoHLLkvDniRJktTlDHrdZCHoNUoUkjzlUvd19ACelHkCOzMPsWfLbTz88Ak88Od/Hv7hH+D++1tVmiRJktQWDHrdpBn05ptBr1ik6xZjAciGDFfnrmTble9f+jw9gA0b4CUvgTe+sWW1SZIkSe3AoNdNpqfToFcvUwg5SqXuDHoAT88+hT3r7uQzd9x9Yg/8qZ+Cm26Cz362NYVJkiRJbcCg102aq27O1osUku4OermQ44pwBR/t/8DS5+kB9PfDb/92uuXC3r0tq0+SJElaSwa9brJo1c18yHZ10AO4Zvgydp3xbb52/7YTe+ATnwhPfzr8+q+3pjBJkiRpjRn0ukmzozdfL6cdvTIUCmtdVOv0J308as/TeNNd/3LiD/6lX4JvfAP+3/9b+cIkSZKkNWbQ6yaLVt3MhRzVCmSza11Uaz0zXM7Xk5u4p7jjxB7Y1wdveEPa1du1qzXFSZIkSWvEoNdNmkM3Z+tFso08uTxkMmtdVGs98rRBNtz+dP7wvn888Qc/5jFw9dXptguNxsoXJ0mSJK0Rg143mZ1NF2OpFcnGbFfuoXeowUF45INX8tk9/8kP5u478Qu85jXw4IPwzneueG2SJEnSWmlZ0AshvCWE8JUQwk0hhMcsOj4UQrguhPDVEML1IYSR5vG+EMIvhRA+1aqaut7cXDpHr1Eiqee7en7eYmdv7uNJU1fy+/f9w4k/OJuF3/99eNe74MYbV7w2SZIkaS20JOiFEC4HNscYnwn8KrC4XfJ64FMxxiuAG4Brm8d/BwjAxlbU1PVihPl56O9nrlEiqee6esXNxU4/HQa+8wy+Mf0DvjVzx4lfYNOmdMuFn/op5+tJkiSpK7Sqo3c1cB1AjPE2YN2i+64CPtL8+qPAZc3z3hpj/PsW1dP95ubSvRQyGeZqJUK1d4LeqafCrh15fnL82fzufcv8Frr0Unj2s+GVr4R6fWULlCRJklZZq4LeJmD3otu1EMLCcxVijNXm1xPA+FIvGkJ4bQjhlhDCLbt37z7+A3rJvn0wOgrAfKNEqOV7JujlcrBlMzxy4lJ+NHc//7HvO8u70GteA5OT8Na3rmR5kiRJ0qprVdCb4uAA14gxLixr2FgU+sY5OBAeU4zxPTHGS2KMl2zc6AjPg+zdC8PDAMw1SoRqnlxujWtaRaedBnfdkeWXT3khv3n3X1GLy+jKZTLwe78Hf/3X8KUvrXyRkiRJ0ippVdC7EXg5QAjhQmD7ovtuBl7S/PplwBdaVENv2bdvf9Ar1stQzZLrkY4epPP07rgDrhh9PANJgb/d8YnlXWjDBvif/xNe/WqYmFjZIiVJkqRV0qqg9xkgH0K4EXgX8MYQwjtCCHng7cBrQwhfBi4GlrEBmg6zdy8MDQFQbFSol/Pke6ijt2EDzM7A1FTg1097CW/e+s/sqU4t72IXXwzPfz68/e1Qq61soZIkSdIqaEnQizE2YozXxhgvjzG+IMa4Lcb4xhhjJca4J8b4/BjjlTHGX44xlg957KWtqKnrNYNeNdaoxzr1coZ8j2yvAOmoyzPPhFtvhXP6TuGqsSfye/e+d/kX/JmfgUoF3v3ulStSkiRJWiVumN4tJiZgaIi5eon+pEC1EnpmMZYFj7oAvv71dKeJn9vyPD6+52t8e+bO5V0sk0m3W7j+erj55hWtU5IkSWo1g1632LsXRkaYb5TpyxQol+mpoZsAp58G80XYtg2GMv289tQX8sofvYWZ2vzyLjg0BD//8/BHf+R8PUmSJHUUg163mJiA4eG0oxfyVKv01NBNgCSBR18AN92U3n7u+CVc0H8Gv3THnxFjXN5FL7gAnvpU+MM/hEbj+OdLkiRJbcCg1y0mJ5tDN4v0ZfJUKvTc0E2ACx4N3/selErp7d887aV8f+5e/veOjy3/oj/2Y2nH9P3vX5kiJUmSpBYz6HWLffsODN0MvRv0hgbTrRa+09wzPZ/k+KOzfo43b/2/fHP6h8u7aCYDv/AL8M//DLfdtnLFSpIkSS1i0OsG9TrMzKQdvUaJvkxz6GYPBj1IR1t+7aYDt08tbOC/n/6T/MQP/pCtpYeXd9H16+FVr0r32JudXZlCJUmSpBYx6HWDqSkYGIAkYb5WohByVCpQ6NGgd8YZMDMN27cfOPb00cfysg1XcPX338De6vTyLvzEJ6Yp8q1vTZf2lCRJktqUQa8b7N0Lo6MAzDdK5MgRI2Sza1zXGslk0rl6X//6wcdftvGZPHHoPF542+9RalSWd/GXvQxuvx0+/emTL1SSJElqEYNeN9i3D4aHAZhtlMiRJ5eDENa4rjV04aPTeXpzcwcff+0pL2QgKfDqH75leStx5nLwi78If/EXsHXryhQrSZIkrTCDXjfYu3d/0JurFcnUc2R7bA+9Qw0NwXmPPLzxloSEN5zxKu4obuNvH/zE8i5+6qnwwhfCG98IlWV2BiVJkqQWMuh1g3370mQDzNZLZBp5cj06bHOxS58Kt94K99138PF8kuWNZ7yKP7z/fdxT3LG8i19xBYyMwF/+5UnXKUmSJK00g1432LsXBgeBdI5eppbv2fl5ixUKcNnT4EMfThcmXezMvs28atNV/Oztb6ce60e+wPH8zM/Af/wHfPGLJ1+sJEmStIIMet1gYiLtLpF29EItnaMnOP+RkM/BV796+H0/seEKSo0Kf7H9I8u7+MAA/PIvw5/8CWzbdnKFSpIkSSvIoNcNJiYOzNGr29FbLAS4/HL4/A3pCNfFkpDwO6e/gj954F+4Y/6B5T3BWWfB858P/+N/QLl88gVLkiRJK8Cg1w0Wrbo53yhB2aC32Pg4PO6x8LGPH37fqYUN/MSGK/iTB/5l+U9w5ZUwNgbvfOfyryFJkiStIINeN1gc9OolYs3FWA71xCfC/fcdvjALwIvWP41P7LmJHeXdy3+Cn/kZuPlm+OAHl38NSZIkaYUY9LrB5OT+OXrzjRKxlCNj0DtILgdPeQpcfz0cun3eaHaQ54xfzF9u/+jyn6CvD37jN+Af/gG+9KWTqlWSJEk6WQa9Tlcup3u59fcDMN8o0ygVHLp5BOefD/PzcNtth9/38o3P5O8f/gzTtbnD71yqDRvg2mvhrW+F7353+deRJEmSTpJBr9Pt27e/m9cgUmlUqZeyrrp5BJkMXHopfOITh2+3sCW/jicPPYr3PPTpIz94qc48E17zGvid3znyOFFJkiRpFRj0Ot2ioDdfL1NI8lRKiR29ozjzzLT5+c1vHn7fyzc+k7/Y/hGqjdrJPcmFF8KP/zj82q+lO7ZLkiRJq8yg1+n27j2wtUKjRF+Sp1KBrB29Iwoh7ep97nOH74Zw/sAZnFrYwAd3r8Acu0svhZ/6KXjd6+CTnzz560mSJEknwKDX6fbtg6EhIF1xcyApUK7gqpvHsHkznHoqfOUrh9/30vXP4H/v+NjKPNHjHw+vfz285z3wrndB7SQ7hZIkSdISGfQ63d69+4PeXL3Z0Svj0M3juPjiNOhVKgcff+rIo7m/tJMfzt2/Mk90yinwhjekK8D87M/Ct7+9MteVJEmSjsGg1+kmJg509BqldI5e1Y7e8axbB1u2pFvfLZYJGa4ev4T3PvSZlXuygQH4zd+EZz4Tfu/30oVatm9fuetLkiRJhzDodbqJif2LsaQdvRxV5+gtyUUXpVveHboC5zXrnsL7d36eaqwf8XHLdskl8KY3wdhYusH6O9+ZdmQlSZKkFWbQ63SLF2Opl8iTJySQ+Moe1ymnwMAgfPd7Bx8/vbCRs/u28M3pH678k+ZycM018Ed/BLt3w0/8BPyf/wOzsyv/XJIkSepZxoFOtyjozTdKZBt58nbzluyii+CGGyDGg49fPX4J/7bv5iM+ZkWMjMArXgG/+7tw553w0pfCv//74YVIkiRJy2DQ63STkwd19DIxSy6/tiV1krPPgloVbr/94ONXjD2BO+a2sbM62doC1q9PF2l57Wvhb/8Wfuu3YOfO1j6nJEmSup5Br5PFCFNTBwe9ep6cHb0lCwGe+MS0q7dYX5Ln8UPn8sk9N61OIeecA//zf6arxLzqVfDpT6/O80qSJKkrGfQ62dwcZDIsJLvZejENeq64eULOOy9d0+buuw8+fsnwBVw/cSN1GqtTSDYLP/Zj6Sbrf/d36WIt7r0nSZKkZTDodbJ9+2B0dP/NuUaJxI7eCctk4LKnwYc+BNXqgeOnFzYylBnkq5PfX92CTjst3XvvBz+AX//1dHiuJEmSdAIMep1s0UIsAHP1IknVoLccjzgXhobhi188+PiVoxfxgZ03HPlBrTQwkIa8jRvTrRjuu2/1a5AkSVLHMuh1sn37Dg56jRKhmifr0M0TFgJc/gz4ylcPXgvlScOPZHt5N7fPb1v9opIkXY3zec9LF2s5dMUYSZIk6SgMep1s714YGtp/c65eAoPeso2MwMUXp0M4F3Y5yISEy0cfz7/u+sLaFXbZZfCTPwm/8Rvw3e+uXR2SJEnqGAa9TnZI0CvWy8RSnqxDN5ftcY9N17j5z/88cOwZo4/jK5PfY6I2vXaFPelJ8HM/B//9v8PNLdzfT5IkSV3BoNfJJiYO7ug1yjTKztE7GZkMPPOZ8IlPwIMPpseGsv1cPHw+/2/3V9e2uMc8Jh3C+bu/C9/85trWIkmSpLZm0Otke/em4w2bivUSjVLO7RVO0qZN8Jznwuf/HX5wW3rsWWNP5CO7v0w5rvF2B+edl4a93/99uOWWta1FkiRJbcug18kefnj/9goRKDbKNEoFO3or4Mwz4GlPg6/dBF/7GmzJr+fcvlP4wM7Pr3Vpadj7xV9Mt2Bwzp4kSZKOwKDXqWKErVvhlFMAKDUqZEKGSikhl1/j2rrE0DBc9ax0I/XPfgZePH45H9h5A7uqk2tdGjzqUfDzPw+//dtw221rXY0kSZLajEGvU+3dm35ubq8w3yjRn+SpVrCjt4L6+tM5e/Pz8KWPjXHpwBP4y+3/b63LSj3mMekee7/1W269IEmSpIMY9DrVfffBaaftvzlfL9OfyVMq4xy9FZbNwlOfCuPrYM9nL+HmqTv57uzda11W6nGPg1e+En7zN9PWoyRJkoRBr3Pddx9s3rz/5ly9RIECpTL09a1hXV0qJPDYx8JjHpVn5HtP54/v/iB1GmtdVuqii+DlL4df//X0+0KSJEk9z6DXqe65J10esmmuUSTbyDM0BElmDevqcmedBdecfQETe+Cd32uDhVkWXHIJvPjFcO21cP/9a12NJEmS1phBr1Pdc8/+hVgA9tVmydT6GBk6xmO0IjZtCvx43zV8YuZL/O1322g/u0svhR/7MfiVX3HOniRJUo8z6HWqRStuAmwv7aZQGmXQoLcqzl4/wk+El/JPxY/wz99uo1UvL7sMXvEK+I3fgG9/e62rkSRJ0hox6HWi2dl0Gch16/YfeqC8k2RmlGGD3qo5b916fjy8iL8pv4/3fPFe4loXtOCJT4Rf+AX4nd+BG29c62okSZK0Bgx6nei+++DUUw869EB5F419owu7LWiVXDB6Ki/MXc37Bv+a13zqo0zMlte6pNQFF6Tz9d78Znjf+6DRJgvHSJIkaVUY9DrRvfcetOImwI7yHqo7xwx6a+Cxg+dy7dDPMjm4gxd/90188O5vUWuHFTnPOQfe+Eb4whfSoZwLey9KkiSp6xn0OtEhQa8Sa+ytzZDMj7i1whoZyQzymlOu4Yryc/mbrZ/h2be8gXc+8CF+NL91bYd0jo+nG6pv3AivfjV8s40Wj5EkSVLLuLV2J7rnnnTvtKYHy3sYCyOMDicQ1q4swVNOPYPHzL2Sr966l29uvJ0vnvF35DIJzxl/Es8dv4RHD5y1+i9RkqRbLzzykelQzrPPhv/23+DCC1e7EkmSJK0SO3qd6P77D15xs7yHodoYQy7E0hYGB+Gap6zjKfWnseXfXsPTp5/Pnuo0b7j33bz8B/8fH9/zNcqxtvqFPfrR8KY3pYHvda+D3/5t+P73IbbNMjKSJElaIXb0Ok2pBBMT6VC8pu2V3fSVRg16bSQkcP75sGVz4L9u2cTg7Zt4/dVP48HcNj418XX++sHr+Yn1z+AF6y/lnL4tq1dYNgtXXJHuufeVr8Dv/34a9K65Jv14xCMg2BaWJEnqdAa9TrN1azo/LznQjN1W3kWYHTHotaGRUXjWlXDnnfCBDwQuv/xMrn3cmeys7uVr07fyK3e+iw25UZ43/mTO6dvC5vw4m/LjrMuOtHaIZz4Pz31u+rFtG9xyC/zmb0K9DhdfDE9+cjo8+Kyz0nAoSZKkjuJPcJ3mvvsOGrYJ8EBpF429j2D4zDWqSceUZOCCR8Mpp8K3boFvfBMuvHAdV134TH7inMu5c347t87dy9embmOyNsOe6hSj2SGeNXYRV409kccNnUvSyth3xhnpx0tfCnv2wB13pN2+f/zHdKXOM89M25PnngubNqW/aNi8GcbG0nGqdgAlSZLajkGv0xxxa4XdZPc8ieHHrFFNWpLRUbjq2TA5mTZmP/hBGBlNeNT5Z/Lc889kbFN6XoyRbeVdfG/2Hv7o/n+kL5Pnj8/+RR7Vf3rri9ywIf14+tPT2+UyPPhg2vW78074r/9K/wB798LMDFSrMDQEIyPpcOJNm2DLlrQTeOGF6cIvmUzr65YkSdJBDHqd5p570sU0mhpEHqrs5fzKKLn8GtalJRsbSz8e91jYtRt27Ejz0+AgPO5xcNFFgTP7NnNm32ZeuP4yvjn9Q6698y/4yY3P5JdPeQG5sIpv20Ih3Y/vnHOOfH+tBvPzMDubBsCFEHj77fDud8PUVPr9euml6dzARz3KDqAkSdIqMOh1mvvvh8sv339zV2WSAn2MDZryOk2SSZtfW7bAEy9K19i5/Xb43vfgOc9NR1OGELhs9DFcMHgmH9z5Jb6w79v82qkv5KrxJ5Fph0Vzs9m0mzcyAqeeevj9c3Pp9+yPfgSf/GTaAXz60+Gqq+ApT0nnCkqSJGnFGfQ6Sa2WDqPbcmCVxu2V3Yy4tULHSzKwcVM6+nH7dvj0p9Ogd+WV6cjI8ewwv3bqi7l17l7+/qHP8n8e/AS/uOX5PGP0cazLDq91+Uc3OAiPeUz68fKXw86dcOut8Dd/k674eemlaei79NJ0bKskSZJWhEGvk2zfDuvXH7QK4vbSLgolg17XCHD6GWmW/9GP4J/+CZ76VHjSEyGTDTx+6BE8bvBcbp/fxif23MS7tn2Y4Ww/jxk4m2eMPo5njz2JwUzfWv8pjm5hIZfnPAemp9P25Yc/DG99a7q1wzOeAZddBhdc4Nw+SZKkk2DQ6yT33XdQNw9gW3k3ycwIw23c1NGJy+bgcY9P1zL53vfg+99LG19nnQVJJvDowTN59OCZxNhgV3WSe4sP88mJr/Pn2z7MM8Yex8s2XMEThx7Z2i0aTtbISDoM+fLL0271nXfCD3+YtjMnJ9PtHZ76VHjSk+C88wx+kiRJJ8Cg10luuin9yX+RbeVdNPZtYfgRa1OSWmt4BJ5xeTpi9z/+I13oct162Lwp/ZyEhBjXkWMdl/dfyDUb57k7uZ0/uv8fWZ8d4ZdP+TGeMfq49g58kHapL7ww/YC027ewyud116WLujzucWnoe/zj0/MGBta2ZkmSpDZm0OsU8/PwhS/AH/zBQYcfKO2mse8CBh262dVOPTX9qFUPLG750ENAhIUUVy7Dvq8PMD/3JB6x4SIyF9zFO8sf4S+z/4/LRx/PU0cezUVD59GfHHsBlEqsMVmbpR7rNGKkQWRDbvS4j1tRIyNwySXpB6QJ96670vD3+c+n2z2cfnq6iue556a/ADnrLBgfTyc1Hm+T9xhd/VOSJHU1g16nuOGGdPja2NhBhx8s7+G8xqij2npENgcbNqYfR1OtwORkwo6HHsXG/zqfysYH+f55W/na8Md4KO5kKDPASKafkcwgmZBQblQpxSqlepnJ2iylWGE4M0AmZPZv1D5Vn2VddoRz+k7hkqHzefGGpzOeXcXfLgwPp928Jz0pvV2rpWFvx450g/evfQ0efjjd5mFuLt0Woq8vDXT1evrRaBz4Okbo708D5egorFsHj3502il89KPTeYQGQUmS1MEMep3iox9Nl2BcZKo2Rz1Gxvv716YmtaVcvrmC5yZ4wuMCE3tPY/v203hwB4xlqpx+fpFNZ5ToHymRzUVyIUsuyVAIeUYyA/RnCoRDQk4jNthdneTBygTfmr2Tf3j437hi7PH89KZn8+iBs1b/D5nNHn1/vxjT9maplM7rS5IDHwu3Q0jvXwiGk5NpcPz2t9Pd7LPZdFGYpz89nSfoJFhJktRhDHqd4O67027FYx970OHt5d0M18cZGrTzoCMLCWzYkH5c9HiYnMqxY0eOO24cYe/etKG1sJffho0Q1kM4wtS3JCRszq9jc34dTxx6JD9Rm+cb0z/gdXf/NZcMP4rfOv3lbMqNrfqf74hCSLt5fcdZfbS/P/3Y2GyPXnTRgft27oQf/AD+9V/hzW8+sCLo05+eDhdN2mAPQ0mSpGMw6HWCj3887S4c8sPl9soe8nOjDNls0FKEdOTv2BjwGGjU0zVP9uyFBx6A226DfZOQy8GWzXDKqXDKFti0Cfr6Dx7JOJQd4LnrnswVo0/g3/f9Fz/1wz/mZzY/h1duvKq9t3dYqoVtIK66Kt3k/c470/0uPvWpdL7gYx8LT3hCukDMox9tx0+SJLUdg167K5fh3/4N3vCGw+76wa6dVPaMcMZ5a1CXOl6SgbHx9GO/CHPzsG8v7NmTrn+yb186vW2gHwYG08+FAhT6oFDIc/bI0zln7DF8Y/LrvP/hG/ixDZfyyo1XcUbhGBMJO0kud2DTd0iHed57b9pp/9KX0qGehQKcdhqceWa6SMyWLWlQXGiXOrxakiStMoNeu/uP/0h/eNyw4aDDpUaV6ydu4slDV1EorFFt6j4BBgfTj9PPOHC4Vk2ntJVKUK6kC75Uq+n0tj17YHZmjMr0Czitb5qvn/d9rt/8dsbCKOflzuKC/rM4f/BUzhpexyl942RilkYjDY+FQjodrqMGH4+NHbwwDKTbP+zalQ75fOihtPs3OQl7m4l5YCANfqeeCmeckYbB005L26VjY+mCMIeuqFSrwcQE7N6dXnvXrvTrnTvTr4vF9EWo1dJ5iUND6VjcsbH034uF51gInsdbiVSSJHUV/+dvdx/9KFx66WGH33nrv5Of3sDTTj9zDYpSr8nmYCjHsYcJRyiVRpicfgaTD17G9uouHmY3d/Xdzlzf16kUZqj2z5Cp9JOfHyVfHCM3M05hegNDpQ2sq23kkeMbeNSZg5xzdpqH+jtlFOjoaPrxyEcefl+M6XDPiYk09O3Zk64SumdPGhCnp9PtUwYG0vGxtVr6Ua+nwW3dujS8LawQunlz+jx9fWl4y2TSxxWLafKen09D5te+lj7nrl3p7S1b0l8anX32gc6jIVCSpK7l/+7t7GMfg/vug1/6pYMObytN8JniF/nx3E+TuK2C2kVI5/Jt6YctmzNcwCnAKQedEmODuf55ZkZmmWGW6TjLZH07k40fcndjim8xRT026HtonOTOEXKZDP2FwEB/QjYbCZkGIYnkMxn6kgL9SYF++hhK+hlI+hnODLAuM8qW/jHOHBllPD9ILhx4k8zUizxUmWBHeQ8PlHaytbyTndV9jGUG2ZgbY1N+nHP7TuXRA2cymh1cob+XkIa0kZEjrxIKaXtzfj79eiG8LawQuhJqtQNdwYcfhptuSoPm7t1pCBwbSwPkKaekXcaNGw+s4jM+fqDrmMutTD2SJKnlWhb0QghvAa5oPsdrY4w/aB4fAt4LnAbsBX4uxjgdQvhx4LeBPPC/YowfalVtba9ahT/7M7j5Znj96w/7bfsffO/DnLbzSTzqkSNrVKC0PCEkDIUhhhg6EAEP+VeoFMtMD0wzPTbPfLHB9ExkdlekVgnUa+nHTKwzmVRpZKrUkwr1zCSNzC5q2TK1/Dzl/CzVwiz1XJEkZsnX+6lnKxAajDHKWDLKumSU9ZkxzstupBxLTFTn2Dp/N5+p3czWysOMZYc4Lb+BgUwfg5k++kKeCEQaBBI25EbZkh9nS34dZxQ2cUphHRmWGcySBIaGmG+U2VbezWRplun6HLO1YlpHYQOn5Tcsf6GbbDYdNnrqqYffV6+nYW/fvrQDODmZrjg6M5N2HGdn04+ZGcjnD4ztHRxMu5D5fPpRKBwcTBfvYVirpWF2YWuLJEnP7+9PrzE4mC5oMzycBuLh4QPHBwfTgJnNHtgmo1ZL/50sl6FSSUPywkexuGiccTl93sV/z3196bUHBtLhrgvd2JERO5uSpK7Skv/VQgiXA5tjjM8MITwWeCfwgubdrwc+FWP81xDCbwDXhhD+Gvgd4NnNmr4WQvhEjLHUivra2sQE/M7vpL/Nf8MbDlsi/osP/5C7qlv5hY0/12ETm6Sl6QsF+sJGNiVADljm7zMadSiVI9OlKpOlErX5HNXZPsqlQK2ZPfbWYU/z63pzP/VQg9PrDRojk+wZmoZchZirQrZKJhPIZgO5bIPb+yeo9W2lkp9lOrOXeeY5NbeR0/s2sik/yqb8KGO5YfpCnr4kRz7k00xSbjBfajBZnmdPdYrdtX3sjhPsSh5iLsyyPqxjIOlnIFNgMJunFEpM1NLzhjMDPLr/LB47dA6P6j+DUwvr2ZJbd1AAjLB/DmS9nmabbBaSo/x7ETMZaqPrKRXWw5bz0jmT2QbTjWkmalPsqU4zXZ9jujbHdGmapFZnoB7or8JQLcNYI8doLctALVClTpk6JWpMUGRPpsSeUKKaNMiRIU+G4ZjnrDjCWbUBtpSyhLl5wr59hIWAViymgW0hrM3PHwiKC3+obDYNfwsfC9tp9PUdCJ4L9y0On41GGgwrlTQEzs+nw11nZtLP+Xwa/oaGDoTYxddZWHp2IawuHAvh8JoWwu/C7YUu7UKYjDH9aDQODNet1dLaqtUDnxfmYS78HSwWwoHnWAiww8Np/cPDaYBd6MaOjuKE7iOo1w98zy183y18rzUa6d/twlYsC794CP7nK6kztOrXl1cD1wHEGG8LIaxbdN9VwJ82v/4o8HfALcAXY4xloBxCuBm4APhui+prH1NT6ZLtP/hBuoDD9u1w+eXwwhfu/4HkM/fcz+d2/og7w33s2Xg/F+25guzmfUxOHv2y/XNFdu95cNX+GN1oaGovxVpxrcvQSerLwJZBYLAMG2eX9JiFsFSvD9JoDBIX/dxXrqaL01T3pllh4WO+WmU2P8n9AzPcVZijVthNPV+ikanTSGrEpA5AIJCEQK6Rp1AboK82wEBlI48qnk9+fphGPVCvQaUK81VoRBgFRomUB2a5d2wXt43+iPLw16kMzFLLl/YXndSzJI0soZ4QYkJoZAiN9HPSyBBi+gNqDJEYGsSkQUzqxEydeqZKPVchJgfCRK44SKHST77eR75RIB/zJJlII1OjnqlRTSpUkhKlTIlatkKmkSVpZMjUc+SqfeQqA2QrfVDL0KBKjTK17D7Kg3dSGt5HHGmQ7SvQNzNOX3UdmUKekM+QHRslZgepF0rU8oPUcxUaSY1GpkYjqUGIECCGOlAnUiQSF72C4cALycKfuQE0iEncf3cI6ZcJCUkcIBsDmVghE/eRNCbJxvSpMo1AppGQbSRkGxlyjQz9tRx9tSwDtSz9tSz981kGagmFOuTqkVwjkmnUiKFOPdSpJw1qSY1qUqOSjQfKDIEMCbmYJUeGLBlCkiWEdOhuNROoZiLVHNSTSA2ohzohhrSeKuSKkcJEpK9Sp69Sp1CtkKtU6K+UyFeK5CpzJM2njCFDvW+ARt8gFPpoFPpo9PVDNktMsjQyGWKSoREbNBqRWmxQjQ3KjRrVWGM+VJlPahSzdeaTGqVMjflsnWqm+Qok6Z+pv5GjELP0NTL013MM1LP013MUGhly9YRCIyHbgEyjQdKok200CPUqmXrzDdaoEGsVqJepNypUY4VKqFHJRIpZKOaglIVqBqpJ+tEIEJMMMSQEErIkZGOGXCMwUI3016C/2qC/XGWgVKVQg2yEpJG+L8kUiNls84VJ574mjTpJrUxSq5DEA99l1f5BGv1D1Pr6qfYNUCv0U83mqIRIOROphEitXqYSS1RjiXq9ArUyoV4hqVXI1arkGpBppN9jMTT/3Umgmkmo5rI0MjlCkiNkciQhS44cefLkyZJpQBIDSQzERp16rFGjRpV6+vcU6lRDA4iEGAgRco1Arp4lFzMUyKa/eknyZJICIVcgyRYgWyDm88RsHpIsZBJCNgMhIcQGkXTxp0a9RqNRpl4vUa9XqdZL6Z+VcrOKOg3qECO5GMiRaf6yJ0shyZFP+slkCmRyBZKkALkCjUwBsjkaIUsjydEgQ4NArAcaEWKMxHrjwD/QNH9ZsvBeDxAJNEIGmp8bSZYYEhpJhhgWhsQHQiaTTm9OAplsIISY/jIsRgLN0QiNevMXMXWSRu3AR6yR1GtkaB6PdUJsQKNOaDQINJq/x4npZ5oDHNJXgzpQo0EtRKohUk7q1DJ1KkmDaqZBLWlQTyJJkiGTZMiELLlMnnxSoJD0kc3kyWYKZJMc2WyBkKTfs7kkx5nZ09JfQDUahEb6Zwi1GkmlTKiUCZUSSblIMj9HUpojKc6RlOYJpWL6uVKC+oHHxiQDuTz1bIGYK1DL91EvDFErDFDL9VPPFqhlCtSzBeqLXrN6zBAbjfT1asT077Ke/j1lQ51saJDNNEhCJJs0SDKQTdJ/P0Jo/mIyJM3XM6T/JoUsDTLUQ4Z6yKa3Mwv/bmXTX6JlsyTZBJIMdRJiSOup1QO1ekJ14XdmMRBDhnu3Hfh9WaGQ/r5s4XdnC7/nW5gGnyTpzIbTTlvSjxFto1VBbxOwe9HtWgghiTE2gEKMsdo8PgGMH+H8heMHCSG8Fnht8+ZsCOGOFa98lW2C9WfA2Qu3I8TGjTfWufFGABrA9085+HX6XuOr/PNxrhuLEFzRvWv5+navY762RdJ/HQ/RSJqZhlrz4+Rk0jGqwFzzY6lO7LljgEYoAw83P3rAPDCwys950NTKOtRnYG7mxF7ajlFvfixBYCHpk37Dl4780IR0Uslijbm0C3zo3+GKvL4NoNL8UFtZi/fvCbhgDwxWj3+eoEg/P3zvOw85uhs43tZQ3/pWi0o6GWcd7Y5WBb0pDg5qjWbIA2gsCn3jpH+rU8Di3eAWjh8kxvge4D2tKbm7hBBuiVPxkrWuQ63h69u9fG27Wwjhljjp69utfH27m69vdwsh3BLj1q56fVdoSbfD3Ai8HCCEcCGwfdF9NwMvaX79MuALwH8C14QQciGEAeCxwO0tqk2SJEmSulqrgt5ngHwI4UbgXcAbQwjvCCHkgbcDrw0hfBm4GPjHGOMe4J+ArwGfBd4UYzz58UeSJEmS1INaMnSzOSzz2kMOv7H5eQ/w/CM85r2k2y5oZTjEtbv5+nYvX9vu5uvb3Xx9u5uvb3frutc3xBiPf5YkSZIkqWO0auimJEmSJGmNGPQkSZIkqcsY9LpMCOEtIYSvhBBuCiE8Zq3r0coIITwUQvhy8+PVIYRHhRC+2HydD90IRm0uhLAxhPC2EMJbmreP+Hr6fu5MR3h9fyuE8KPm+/fzi87z9e1AIYSxEMIHm6/nV0MI5/ge7g5HeW19/3aREEI+hPCp5uv5lRDCad38/m3VPnpaAyGEy4HNMcZnhhAeC7wTeMEal6WVcXeM8cqFGyGEfwN+KcZ4fwjhIyGEp8YYb1678nSC/hy4mwNb7/4lh7yepFs0+37uTIe+vgB/EGP86MIN/73uaAPAf48xPhhC+DHgd4Bz8T3cDY702t6F799uUgN+KsY4H0L4GeDngcvp0vevHb3ucjVwHUCM8TZg3dqWoxW0b+GLEEIO6Isx3t889FHgsrUoSssTY/w54KtwzNfT93OHWvz6LrLvkNu+vh0qxvhgjPHB5s19QAXfw13hCK/t3KKvF/O17VAxxkaMcb5585HArXTx+9eg1102AbsX3a6FEHyNu8OZzeEDHwFOBSYW3TcBjK9NWVoBGzjy6+n7uXsUgT8JIdwYQvi15jFf3w4XQjiNtOPzLnwPd5VFr+1f4vu364QQ/kcI4S7gEuDbdPH716Gb3WWKg3/gbzT3NFSHizFeBBBCeBbpDxVji+4e5+B/jNRZpjjy69mP7+euEGN8N/DuEEIfcH0I4Ub897qjhRBeCLwI+BXSIDC26G7fwx1s8WsbY5wAfP92mRjjO4F3hhCeD/wFXfz+7bhkqmO6EXg5QAjhQmD72pajlRBCyCy6uQ+IQKH5G0eAnwC+sOqFaUU0h5Ac6fX0/dwlQggLv1QtA/Ok72Ff3w4VQng88KIY46/GGCd8D3ePQ1/b5jHfv10khDAcQgjNmw+QZqGuff/a0esunwFe0Pxt0wzwq2tcj1bGmSGEfyH9T6YCXAusB/5fCKEMfDLGePtaFqiT9t855PUMIdyJ7+du8eYQwjOAHPCxGOMPQwi34+vbqa4BLg8hfLl5+wF8D3eLI72223z/dpULgL9svleLwG+STqHoyvdviDGudQ2SJEmSpBXk0E1JkiRJ6jIGPUmSJEnqMgY9SZIkSeoyBj1JkiRJ6jIGPUlSV2ouo/2sFbzeaSGES1bqeidRx0uWcM4TQwj/fTXqkSS1J4OeJKlthRDuCCF8+ZCPuw855wshhG+FEO5qfv2EEMLnSLch+elF5z01hHBjCKHcPO8LIYRSCOGmEMLTFp03EEL4QAjhqyGE60MIG5p3PZJ0+fWl1P3tY9wXQgh/EEL4SgjhhubnP1i0t9Pic18ZQnjNIYf/26L7H3XI380DzbsKwMhSapUkdSf30ZMktbP7YowHhatmiNsvxvicEMKVwKUxxj9tnnOka90CvAj4Z+Cnmsc+CPwysG/Rea8DvhRjfF8I4SrgrcCvLbXg5ua6TwwhPDbGeNsRTvlN0v9/r4wxxmbAe1Pz+P8+5NxM8+OIYox3AFc2n/cRwNuWWqckqbsZ9CRJ7ezsEMIXDjl21hHOWw+MhRAeC1zEkbtZlwAvBX4E/H/NY7cDvwN8AvhG89jTgB8HiDF+KYTwxqUWG0IYBf4R+GPgfSGEq2OMk4ec9mTgzbG5kW0z7L2fNOwd6gxgYIlP/yfA/1p0+7EhhJfGGD++1PolSd3DoCdJalsxxguWeOoTgccCDaAGxMV3hhCeDfzuMR5/SQjhz2KMn0+fNtYX3Vc/2oMWXT8LvBD4A+DPYowfDiF8H/hCCOFPgE/GGGvN028A3hBC+O0Y42wIYbhZ2w1HuPQVQP44zx2APwW+E2O8+Xi1SpJ6g0FPktR2QgjPBX5/0aEM6bzy6qJjfxpj/FwzZD0RuB+YjTF+8NB5bTHGLwJfDCFsal7nZaT/B34IaMQYdy06fTaEsC7GuDeEkGNp89kfBzwVeHGM8cEQwlNjjB8NIXyNdEjmPcD3mrW8v7mgyqdDCA0gABMxxvcf8nfwIuBmYFcI4TdjjH99hL+ni0i7hzfEGA8d9nmb3TxJ6l0GPUlS24kx3sCiDlcI4YXA2UcKO6Rz6j5AGqT+BPiZY1z6l4DBRbd/k3SY5mMXHXsP8K4Qwh8D1wLXLaHe7wDfWXTobcBzYow7gT88wkMmgd+JMd4fQjidA0NJAQghPBn4VeAnSMPt+0MIMzHGfz7kOuuB344x3nW8GiVJvcWgJ0lqWyGED8cYXwEUgdkj3H8WcEmM8VXN2zeGEB53jEteAowecmx48Y0Y45ebi7lcC3wjxnj98v8Ey/YE4OdijBWAEMIvAM889KQY4xdDCE8OIfxejPFPFh3/JvDNVatWktR2DHqSpHa2DvYPvTxMjHFrCOHVi26/G4666ibAYIzxOcd70hjjl4EvL7XIEMK/AKcdcmzx4x+OMb7ykPP+aXGdzfMfjjG+Msb494fUUwUOXZRmQYbjzOOTJPUeg54kqZ094QirbkLa7XoQ0pVTTuB6jzokgC345Rjj3Uc4viQxxp8+/llLP28ZXtPcYmKxW2OM/+0I50qSekA4sf8fJUmSJEntbikriUmSJEmSOohBT5IkSZK6jEFPkiRJkrqMQU+SJEmSuoxBT5IkSZK6jEFPkiRJkrrM/x/EyAXqkrVxrQAAAABJRU5ErkJggg==\n",
      "text/plain": [
       "<Figure size 1080x720 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "sns.set_palette(\"Set1\")\n",
    "plt.figure(figsize=(15, 10))\n",
    "sns.kdeplot(x1, color='blue', label='한글', bw=0.1, shade=True); sns.kdeplot(x2, color='red', label='영어', bw=0.1, shade=True); sns.kdeplot(x3, color='green', label='수학', bw=0.1, shade=True)\n",
    "# plt.vlines(-14, 0, 0.08)\n",
    "# plt.vlines(34, 0, 0.08, linestyles='--')\n",
    "plt.axvspan(xmin = 34, xmax = 298, alpha = 0.2, color = 'red')\n",
    "plt.axvspan(xmin = -14, xmax = 0, alpha = 0.2, color = 'red')\n",
    "\n",
    "plt.legend(loc = 'upper center', ncol = 3)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 393,
   "id": "8af77d3a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "x1 : 15330, x2 : 4883, x3 : 6287\n",
      "F통계 : 372.00478295528444, pVal : 4.6452361716217866e-160\n",
      "0.0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005\n"
     ]
    }
   ],
   "source": [
    "F_statistics, pVal = stats.f_oneway(x1, x2, x3)\n",
    "print('x1 : {0}, x2 : {1}, x3 : {2}'.format(len(x1), len(x2), len(x3)))\n",
    "print('F통계 : {0}, pVal : {1}'.format(F_statistics, pVal))\n",
    "print(format(pVal, '.160f'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 460,
   "id": "333dcbbb",
   "metadata": {},
   "outputs": [],
   "source": [
    "pledo['아이 성별'] = pledo['아이 성별'].replace('MALE', 0).replace('FEMALE', 1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 461,
   "id": "3c9fd229",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([0, 1], dtype=int64)"
      ]
     },
     "execution_count": 461,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "pledo['아이 성별'].unique()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d5c15c20",
   "metadata": {},
   "source": [
    "<h1> 과목별 상세 정오답률 분석"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "13864779",
   "metadata": {},
   "source": [
    "<h1> 한글"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 63,
   "id": "71f66642",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th>정오답률</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>컨텐츠 분류2</th>\n",
       "      <th>정오답</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">가나다 익히기</th>\n",
       "      <th>1</th>\n",
       "      <td>10653</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>2237</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">두글자 놀이</th>\n",
       "      <th>1</th>\n",
       "      <td>1453</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>435</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">세글자 놀이</th>\n",
       "      <th>1</th>\n",
       "      <td>426</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>135</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "              정오답률\n",
       "컨텐츠 분류2 정오답       \n",
       "가나다 익히기 1    10653\n",
       "        0     2237\n",
       "두글자 놀이  1     1453\n",
       "        0      435\n",
       "세글자 놀이  1      426\n",
       "        0      135"
      ]
     },
     "execution_count": 63,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "percentage = [17, 23, 24, 83, 77, 76]\n",
    "korean_course.groupby('컨텐츠 분류2')['정오답'].value_counts().to_frame('정오답률')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 64,
   "id": "744ae2d5",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.legend.Legend at 0x1b0138909a0>"
      ]
     },
     "execution_count": 64,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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bJXa6zVvterVV1/l6KOP5re//S2PP/441157LSNGjGDp0qWceOKJzJw5kwcffJCTTz65KdSPPPJIpk6dyu2338706dP55Cc/ycKFC/nnf/5nvvCFL3Dvvfc2+FlJUse99NJLbLfddk3BDbDtttuy3Xbb8dJLL6103cxk9uzZTWfsq8Izb7VqypQp7LLLLnz4wx8GYNiwYSxatIhnn32Wj3zkIwB86EMfYuTIkUydOpVBgwY1rfvCCy8wceJEbrnlFvbaay/uuOMOevfuzV577cUee+zRkOcjSatq880355lnnmHevHmst956AMybN49nnnmGzTffHIChQ4dywgkn0KtXr6br2eeffz4RwWGHHdYp7TC81aodd9yRs846i7feeov3ve99zJo1izlz5rBkyRIWLlxI//79WbBgAXfddRfjx49vWm/p0qV89atf5ZJLLqFXr168/fbbTdfIFy1a1KinI0mrrG/fvnzrW99i5MiRbLnllgC8+OKLfOtb32p6nxs3blzNdVvrSu8Iw1ut2n777TnrrLPYd9996devH0uXLuW6667jmWee4bDDDmP99dcH4Ctf+QqDBw9uWu+73/0uBx10EMs+BW7MmDEMGTKEtdZai5NOOqkRT0WSOs1uu+3GpEmTuOaaa1i8eHHNEeSHHnooP//5z9ss6yjDWyt1yCGHcMghh6xQPnz48FbXaRnQRx99NEcffXSnt02SGqlv376t3ub16quvstdeey1X9rvf/a7T9m14S5JUh8mTJ3P++eevUP6Tn/yk6edTTjmFvffem759+zJp0qTl6u27776d1hbDW5JUnHpv7epMe+65J3vuuWdddRctWuSZtyRJJZk8efJq3b73eUuSVBjDW5Kkwtht3sMsWLB6u2q6m7XXru/6kyT1JJ55S5JUGMNbkqRV9NRTT/Hkk0+utM6xxx7bafuz21ySpDrtvffevPfee8ycOZOPf/zjbLbZZlx//fU8/PDDLF68mO23396PBJUkqZbOHt9T7/iZu+66i4ULF7L11lszefJkJkyYwNChQ/nzn//Mqaee2lTPjwSVJKkb+d73vscZZ5zB+eefzzHHHMOUKVM4/fTT21zPjwSVJKmLvffee1x44YVstNFGfOUrX+H666/nS1/6EldcccVy9fxIUEmSuoklS5aw8847s88++wBw2GGHsc8++9CnTx8G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pw8bNozBgwfTr18/zj333NXeZqk7isxsdBvqMmjQoGw5MrVel0+f1smt6b6O2nHNOhNZe+09G90ESVotIuKRzBxUa5nd5pIkFcbwliSpMIa3JEmFMbwlSSqMo80lrdSCBZMb3YQu4wBIlcIzb0mSCmN4S5JUGMNbkqTCGN6SJBXG8JYkqTCGtyRJhTG8JUkqjOEtSVJhDG9JkgpjeEuSVBjDW5KkwhjekiQVxvCWJKkwhrckSYUxvCVJKozhLUlSYQxvSZIKY3hLklQYw1uSpMIY3pIkFcbwliSpMIa3JEmFMbwlSSqM4S1JUmEMb0mSCmN4Sw121llnseeee/KpT32Kgw46iDfffJNnn32Wfffdl2HDhvHJT36SCRMmNNU/9dRT2X333RkyZAgzZswAIDMZMWIETz/9dIOehaSuZHhLDbb99tszefJkHnzwQXbYYQfOO+88Nt10U2677Tbuuece7rnnHk488UQWL17ME088wZ/+9CemTZvGz3/+c8477zwALr30UvbZZx+22WabBj8bqev8+Mc/ZujQoU1fu+yyCxtvvDEATzzxBJ/73OfYddddGTx4MM8++yzQcw5++zS6AdKabtSoUU0/77zzztx4442su+66TWVPP/00H/3oR+nTpw+9e/dm/vz5ZCavvfYaAwYMYNasWUyZMoWJEyc2ovlSw4wePZrRo0c3PT799NM54ogjWLBgAQcffDDXXHMNO++8M1AJ6OYHvy+++CJjx47lpptuKvLg1/CWuolFixbx/e9/n7FjxwJwyimncOutt7J48WJuvPFGALbddlsGDx7M0KFDGThwIBdddBFjxozh6quvbmDLpcZ7+eWXuf3225kxYwZXXXUVI0aMaApugIjoUQe/dptL3cAzzzzD5z73OQ4++GD2339/AC688EKefPJJfvGLX3DIIYfw0ksvAfC1r32NqVOncuONNzJhwgSOPvpoZs6cyejRozniiCOYOXNmI5+K1BDnnXceY8eOpW/fvjz00EOsu+66DB8+nM985jOcdtppLFq0aLmD33PPPZevf/3rjB07lksvvbTRzW83w1tqsJtvvpmjjjqK//zP/+T4449fYfnf/u3fsttuu/Hwww8vVz59+nReeOEFDjjgAMaPH8+ECRO45JJLOOWUU7qq6VK38Oabb/KrX/2Kww8/HIBXXnmFWbNmcdNNNzFlyhRefvllLrnkEqDnHPzabS410CuvvMJJJ53Eo48+ygYbbNBU/sQTT7DtttvSu3dvXnvtNR5++GG+/vWvNy1fsGABp59+OjfccAMLFy5kyZIl9O7dmz59+rBo0aJGPBWpYa699loOOOAA+vXrB8Bmm23GiBEjWGuttQA49NBDuf7665dbZ9nB72mnncbw4cO58847eeuttxg1ahSTJk3q8ufQXoa31ECPPfYYb7zxBp///OebyjbaaCP2228/Ro0axYABA+jVqxff+c53+NCHPtRUZ9y4cYwbN64p8IcNG8bgwYPp168f5557bpc/D6mRJk6cyAUXXND0eMSIEfz85z/ngAMOoFevXtxxxx0MHjy4aXlPOPiNzGx0G+oyaNCgXDasv70unz6tk1vTfR21YxkvvM6y9tp7NroJPd6CBZMb3YQu4+upPAsXLmSzzTbjL3/5S9OZd2ZyzjnncOedd9KrVy922WUXLrzwQnr37g3Av//7v/P5z3+eYcOGAXDOOedwxx13NB387r777g17Ps1FxCOZOajmMsO7ZzG81dkMb6kxVhbeDliTJKkwhrckSYUxvCWph6k1X35zX/ziFxkxYkTT454yZeiaxPCWpB6m1nz5y9x777088sgjTY+dL79M3iomtdOaNAAS4KgdG90CtVet+fKhMq/A2WefzXnnncdVV10F0JApQx0EueoMb0nqoZrPlz9v3jwOPfRQLrnkEl577bWmOs6XXya7zSWpB2o+X/4+++zDIYccwsknn8zHP/7xFer2lClD1ySeeUtSD3PzzTdz0UUX8YMf/IAddtiBu+66i9/97neceeaZnHnmmcybN485c+YwcuTIpi51KH/K0DWJ4S1JPUit+fL33nvvpk+lA5gyZQoXX3zxcsHdE6YMXZMY3pLUg7Q2X/5NN9200vWcL78sTo/awzg96uq3Jr2eYM16TTk9atdwtHl9nB5VkqQexPCWJKkwhrckSYUxvCVJKozhLUlSYbxVTJIabM27g6HRLSifZ96SJBWmoeEdEedExNSIeCAidmhkWyRJKkXDwjsidgM2zczPAscD4xvVFkmSStLIM++9gesAMvNxYKMGtkWSpGI0csDaJsCcZo8XR0SvzFy6rCAijgOOqz6cFxGzurKBJfoKvB94tdHtUM/ha0qdzddU3T7U2oJGhvebwIbNHi9tHtwAmXkl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\n",
      "text/plain": [
       "<Figure size 576x576 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(8, 8))\n",
    "plt.xticks(fontsize = 12)\n",
    "\n",
    "sns.set_palette(\"Set3\")\n",
    "\n",
    "g = sns.countplot(x = '컨텐츠 분류2', data = korean_course, hue = '정오답')\n",
    "ax = g\n",
    "\n",
    "count = 0\n",
    "\n",
    "for p in ax.patches:\n",
    "    ax.annotate(\"{0}%\".format(percentage[count]), (p.get_x() + p.get_width()/2.,p.get_height() - 30),\n",
    "               ha='center', va='center', fontsize=12, color = 'black', xytext=(0, 10),\n",
    "               textcoords='offset points')\n",
    "    count += 1\n",
    "    \n",
    "plt.xlabel(\"\"); plt.ylabel(\"\"); plt.title(\"한글 컨텐츠별 정오답률\", fontsize = 20)\n",
    "plt.legend([\"오답\", \"정답\"])"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2784aef1",
   "metadata": {},
   "source": [
    "<h1> 영어"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 66,
   "id": "b62bc539",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th>정오답률</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>컨텐츠 분류2</th>\n",
       "      <th>정오답</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">PHONICS(알파벳)</th>\n",
       "      <th>1</th>\n",
       "      <td>979</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>78</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">RIVER CROSSING(문장)</th>\n",
       "      <th>1</th>\n",
       "      <td>924</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>728</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">스크래치(단어)</th>\n",
       "      <th>1</th>\n",
       "      <td>1639</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>541</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                        정오답률\n",
       "컨텐츠 분류2            정오답      \n",
       "PHONICS(알파벳)       1     979\n",
       "                   0      78\n",
       "RIVER CROSSING(문장) 1     924\n",
       "                   0     728\n",
       "스크래치(단어)           1    1639\n",
       "                   0     541"
      ]
     },
     "execution_count": 66,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "percentage = [7, 44, 25, 93, 56, 75]\n",
    "e1 = english_course.groupby('컨텐츠 분류2')['정오답'].value_counts().to_frame('정오답률')\n",
    "e1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 67,
   "id": "4bf3faa4",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.legend.Legend at 0x1b0141e9400>"
      ]
     },
     "execution_count": 67,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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ww8/vFPaYUgLgF//+td873vfIyJYc801ufbaa5k1axZf//rXef/995k5cyYnnXQSRx99NABnnnkmjz76KPPmzePKK69k4MCBZCb//u//zujRo9lyyy279g1J0hLo3bs33/3udzn00EPZeOONAXjppZf47ne/2/ggkrPOOqvuss11gXeE3d3iH//4B+eeey533XUXDzzwAMOGDePUU09l/fXX54477uD+++/n/vvv59RTT2X+/PlMmTKFV199lQkTJnDLLbdw8cUXA3DVVVex//77G9CSuoVBgwZx9913s+eee7Lrrrtyzz33MGjQoEXqHHbYYYstV6+sozyTFk888QS77bYbq6++OlB8wE466SRWXXXVxjrPPfcc22yzDb169aJnz57Mnj2bzGTGjBn069ePZ555hvHjx3Pbbbd11duQpKWid+/ezd7f/MYbb7DvvvsuUvbnP/+507ZtSIuddtqJs846i5dffpkPfehD/PrXv+bNN99k7ty5fPvb3+b2229n/vz5jB07FigGT+y+++4MHjyY/v37c/nllzNixAiuu+66Ln4nkrqjtt4y1VnGjRvHJZdcslj5DTfc0Pj6jDPOYL/99qN3797cfffdi9Q74IADOq0tkZmdtrLOMHDgwJw0aVJXN2OF85vf/IbRo0ez0korcdBBB3HJJZcwderUxvl//vOf+cIXvsC4ceMar880GDVqFNtttx1rrLEGN9xwA5nJGWecwQ477LCs34akbmDKlClss802Xd2MNtlnn30WO8v+85//zOuvv97sMvXeX0RMzsyBTet6Ji0AhgwZwpAhQ4DiXsBbbrllkfkf/ehHGTRoEI8//vgiIT1x4kRefPFFzj77bA488EDuuece3n77bYYNG7bY0aUkdTfjxo1bqut34JiA4qvhAObMmcPJJ5/MaaedxpQpU1iwYAEAM2bM4PHHH2fgwA8O9ObMmcPIkSO54oormDt3LgsWLKBnz5706tWrcX2SpI7zTHo5NmdO5x3BDR36Ld55ZzZz5rzP0Ud/ls98ZlV+9rNrOeywX9Ov36r06NGDSy4ZznrrPc+cOc8DcNppP+KUU/ajT5/i8sSgQZux667b0KdPb8477yud2r6VV96n09YlScsLr0kvxzozBKvOkJZWHMvTNemOaM81abu7JUmqKENakqQ2evbZZ/nb3/7WYh2/qlKStMLo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\n",
      "text/plain": [
       "<Figure size 576x576 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(8, 8))\n",
    "plt.xticks(fontsize = 12)\n",
    "\n",
    "sns.set_palette(\"Set3\")\n",
    "\n",
    "g = sns.countplot(x = '컨텐츠 분류2', data = english_course, hue = '정오답')\n",
    "ax = g\n",
    "\n",
    "count = 0\n",
    "\n",
    "for p in ax.patches:\n",
    "    ax.annotate(\"{0}%\".format(percentage[count]), (p.get_x() + p.get_width()/2.,p.get_height() - 30),\n",
    "               ha='center', va='center', fontsize=12, color = 'black', xytext=(0, 10),\n",
    "               textcoords='offset points')\n",
    "    count += 1\n",
    "    \n",
    "plt.xlabel(\"\"); plt.ylabel(\"\"); plt.title(\"영어 컨텐츠별 정오답률\", fontsize = 20)\n",
    "plt.legend([\"오답\", \"정답\"])"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a3ba5cb4",
   "metadata": {},
   "source": [
    "<h1> 수학"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 69,
   "id": "59469699",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th>정오답률</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>컨텐츠 분류2</th>\n",
       "      <th>정오답</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">도형과 사고력</th>\n",
       "      <th>1</th>\n",
       "      <td>2825</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>443</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">독해와 연산</th>\n",
       "      <th>1</th>\n",
       "      <td>1959</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>328</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">수의 이해</th>\n",
       "      <th>1</th>\n",
       "      <td>654</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>82</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "             정오답률\n",
       "컨텐츠 분류2 정오답      \n",
       "도형과 사고력 1    2825\n",
       "        0     443\n",
       "독해와 연산  1    1959\n",
       "        0     328\n",
       "수의 이해   1     654\n",
       "        0      82"
      ]
     },
     "execution_count": 69,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "percentage = [14, 14, 11, 86, 86, 89]\n",
    "m1 = math_course.groupby('컨텐츠 분류2')['정오답'].value_counts().to_frame('정오답률')\n",
    "m1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 70,
   "id": "f93baa86",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.legend.Legend at 0x1b014511e80>"
      ]
     },
     "execution_count": 70,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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woUL+e1vf8t2220HwJgxY/jMZz5Dnz59Vp5rvvDCC4kIDj/88G5phyEtAKZPn87YsWPZaaedePXVV5k7dy7Tp09nhx12YNKkSTQ1NbHHHnswbdo0Bg8ezEknncS4ceMYPHgw06ZN49RTT+Xiiy9mwIABvX0oktRl/fv356tf/SqHHnooO+64IwDPPPMMX/3qV1de4zx16tQ2121vCHxNOLtbvPzyyxx//PE89NBDPProo1xzzTVMnDiRF154gYceeogZM2YwZ84ctthiC84++2wAJk+ezF133cXMmTN54IEH2GuvvVi8eDHHHHMMRxxxBHfeeWcvH5Ukdc3o0aO5/fbb2Xfffdl777350Y9+9LbTeYcddtjb1murbE3ZkxazZ89m7733Zvjw4QAccMABNDc388Ybb/CRj3yEzTbbDIAjjjiCU045ZZV1n376aW688UZuueUWxo0bx6xZs+jbty/jxo1j7NixPX4sktTd+vfv3+6lUy+//DLjxo1bpexXv/pVt+3bkBZ77LEH5513HvPnz2ezzTbjiSeeoKmpiSuvvJKzzjqLKVOmMHDgQGbOnMnIkSNXrrd8+XJOPfVULr/8cvr06cOCBQtWDgM1Nzf31uFIUpfccccdXHjhhW8r/973vrfy97POOouDDjqI/v37c/vtt69Sb/z48d3WFkNa7L777px33nmMHz+eAQMGsHz5cq699lr22WcfjjzySMaOHUv//v3Zeeed+cY3vrFyva9//etMmjSJYcOGATBlyhRGjRrFwIEDOf3003vpaCStbxq5ZKo7HXjggRx44IEN1W1ubl6rPenIzG7bWHcYMWJEzp07t7ebIUnqJY899hjvfve7e7sZa01bxxcRD2bmiNZ1nTgmSVKhDGlJkgrlOel12KJFd/R2E3rMRhs1dn5IktYn9qQlSSqUIS1JUoOefPJJHn/88dXWWd2jKjvL4W5Jklo56KCDWLJkCY888gh77rkn2267Lddddx2//OUvWbp0KbvvvruPqpQkqbvn3zQyx+XHP/4xixcvZuedd+aOO+5gxowZjBkzhhdffJHPfe5zK+ut7UdVOtwtSVIbLr30Us455xwuvPBCTjjhBGbPnr3y+QWrs+JRla+//nqX22BPWpKkFpYsWcK0adPYYost+OQnP8l1113HJz7xCaZPn75KPR9VKUlSD1u2bBl/9Vd/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\n",
      "text/plain": [
       "<Figure size 576x576 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(8, 8))\n",
    "plt.xticks(fontsize = 12)\n",
    "\n",
    "sns.set_palette(\"Set3\")\n",
    "\n",
    "g = sns.countplot(x = '컨텐츠 분류2', data = math_course, hue = '정오답')\n",
    "ax = g\n",
    "\n",
    "count = 0\n",
    "\n",
    "for p in ax.patches:\n",
    "    ax.annotate(\"{0}%\".format(percentage[count]), (p.get_x() + p.get_width()/2.,p.get_height() - 30),\n",
    "               ha='center', va='center', fontsize=12, color = 'black', xytext=(0, 10),\n",
    "               textcoords='offset points')\n",
    "    count += 1\n",
    "    \n",
    "plt.xlabel(\"\"); plt.ylabel(\"\"); plt.title(\"수학 컨텐츠별 정오답률\", fontsize = 20)\n",
    "plt.legend([\"오답\", \"정답\"])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "id": "6c863453",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "11.204801038062284\n",
      "19.093227792436235\n",
      "11.96298846617318\n"
     ]
    }
   ],
   "source": [
    "print(korean_course['문제풀이 소요시간'].mean())\n",
    "print(english_course['문제풀이 소요시간'].mean())\n",
    "print(math_course['문제풀이 소요시간'].mean())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 71,
   "id": "b8d7250e",
   "metadata": {},
   "outputs": [],
   "source": [
    "percentage = [11, 19, 12]\n",
    "labels = ['한글', '영어', '수학']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 80,
   "id": "95079d9b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Text(0.5, 1.0, '문제별 풀이소요 시간')"
      ]
     },
     "execution_count": 80,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 576x576 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(8, 8))\n",
    "plt.xticks(fontsize = 12)\n",
    "\n",
    "sns.set_palette(\"Set3\")\n",
    "\n",
    "g = sns.barplot(x = labels, y = percentage)\n",
    "ax = g\n",
    "\n",
    "count = 0\n",
    "\n",
    "for p in ax.patches:\n",
    "    ax.annotate(\"{0:,}초\".format(round(p.get_height(), 1)), (p.get_x() + p.get_width()/2.,p.get_height() - 0.2),\n",
    "               ha='center', va='center', fontsize=12, color = 'black', xytext=(0, 10),\n",
    "               textcoords='offset points')\n",
    "    \n",
    "plt.title('문제별 풀이소요 시간')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5a132fc0",
   "metadata": {},
   "source": [
    "<H1> 문제 고유 식별 값 정오답 TOP 10"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "ebaed45c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th>정오답 비율</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>문제 고유 식별 값</th>\n",
       "      <th>정오답</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">1</th>\n",
       "      <th>1</th>\n",
       "      <td>189</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>25</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">2</th>\n",
       "      <th>1</th>\n",
       "      <td>178</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>72</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">3</th>\n",
       "      <th>1</th>\n",
       "      <td>172</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>58</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">4</th>\n",
       "      <th>1</th>\n",
       "      <td>158</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>24</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">5</th>\n",
       "      <th>1</th>\n",
       "      <td>155</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>28</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">6</th>\n",
       "      <th>1</th>\n",
       "      <td>152</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>30</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">7</th>\n",
       "      <th>1</th>\n",
       "      <td>143</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>20</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">8</th>\n",
       "      <th>1</th>\n",
       "      <td>141</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>32</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">9</th>\n",
       "      <th>1</th>\n",
       "      <td>139</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>30</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th rowspan=\"2\" valign=\"top\">10</th>\n",
       "      <th>1</th>\n",
       "      <td>135</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>22</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                정오답 비율\n",
       "문제 고유 식별 값 정오답        \n",
       "1          1       189\n",
       "           0        25\n",
       "2          1       178\n",
       "           0        72\n",
       "3          1       172\n",
       "           0        58\n",
       "4          1       158\n",
       "           0        24\n",
       "5          1       155\n",
       "           0        28\n",
       "6          1       152\n",
       "           0        30\n",
       "7          1       143\n",
       "           0        20\n",
       "8          1       141\n",
       "           0        32\n",
       "9          1       139\n",
       "           0        30\n",
       "10         1       135\n",
       "           0        22"
      ]
     },
     "execution_count": 37,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "pledo_rm.groupby('문제 고유 식별 값')['정오답'].value_counts().to_frame('정오답 비율').head(20)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "0d3b93b1",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "<ipython-input-34-27a9cf509f20>:1: UserWarning: Boolean Series key will be reindexed to match DataFrame index.\n",
      "  pledo_rm[pledo['문제 고유 식별 값'] == 10]\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>시퀀스</th>\n",
       "      <th>아이 고유 식별 값</th>\n",
       "      <th>아이 생년월일</th>\n",
       "      <th>아이 성별</th>\n",
       "      <th>단계</th>\n",
       "      <th>컨텐츠 분류1</th>\n",
       "      <th>컨텐츠 분류2</th>\n",
       "      <th>컨텐츠 분류3</th>\n",
       "      <th>단계.1</th>\n",
       "      <th>단계별 문제 번호</th>\n",
       "      <th>문제 세부 번호</th>\n",
       "      <th>문제 고유 식별 값</th>\n",
       "      <th>학습 시각</th>\n",
       "      <th>문제풀이 소요시간</th>\n",
       "      <th>문제 정답</th>\n",
       "      <th>아이 블록 입력 데이터</th>\n",
       "      <th>정오답</th>\n",
       "      <th>통계 메인 키</th>\n",
       "      <th>향상 능력</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>695</th>\n",
       "      <td>696</td>\n",
       "      <td>129</td>\n",
       "      <td>20180310</td>\n",
       "      <td>MALE</td>\n",
       "      <td>필수 단계</td>\n",
       "      <td>한글</td>\n",
       "      <td>가나다 익히기</td>\n",
       "      <td>NONE</td>\n",
       "      <td>1</td>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>10</td>\n",
       "      <td>2021-12-31 17:57:13</td>\n",
       "      <td>8</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>1</td>\n",
       "      <td>자음 이해</td>\n",
       "      <td>이해력</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>775</th>\n",
       "      <td>776</td>\n",
       "      <td>128</td>\n",
       "      <td>20170804</td>\n",
       "      <td>FEMALE</td>\n",
       "      <td>필수 단계</td>\n",
       "      <td>한글</td>\n",
       "      <td>가나다 익히기</td>\n",
       "      <td>NONE</td>\n",
       "      <td>1</td>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>10</td>\n",
       "      <td>2021-12-31 21:52:37</td>\n",
       "      <td>5</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>1</td>\n",
       "      <td>자음 이해</td>\n",
       "      <td>이해력</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>800</th>\n",
       "      <td>801</td>\n",
       "      <td>128</td>\n",
       "      <td>20170804</td>\n",
       "      <td>FEMALE</td>\n",
       "      <td>필수 단계</td>\n",
       "      <td>한글</td>\n",
       "      <td>가나다 익히기</td>\n",
       "      <td>NONE</td>\n",
       "      <td>1</td>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>10</td>\n",
       "      <td>22-1-1 9:11:11</td>\n",
       "      <td>5</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>1</td>\n",
       "      <td>자음 이해</td>\n",
       "      <td>이해력</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>821</th>\n",
       "      <td>822</td>\n",
       "      <td>128</td>\n",
       "      <td>20170804</td>\n",
       "      <td>FEMALE</td>\n",
       "      <td>필수 단계</td>\n",
       "      <td>한글</td>\n",
       "      <td>가나다 익히기</td>\n",
       "      <td>NONE</td>\n",
       "      <td>1</td>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>10</td>\n",
       "      <td>22-1-1 9:16:06</td>\n",
       "      <td>10</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>1</td>\n",
       "      <td>자음 이해</td>\n",
       "      <td>이해력</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>845</th>\n",
       "      <td>846</td>\n",
       "      <td>128</td>\n",
       "      <td>20170804</td>\n",
       "      <td>FEMALE</td>\n",
       "      <td>필수 단계</td>\n",
       "      <td>한글</td>\n",
       "      <td>가나다 익히기</td>\n",
       "      <td>NONE</td>\n",
       "      <td>1</td>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>10</td>\n",
       "      <td>22-1-1 9:22:08</td>\n",
       "      <td>12</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>1</td>\n",
       "      <td>자음 이해</td>\n",
       "      <td>이해력</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>36948</th>\n",
       "      <td>36949</td>\n",
       "      <td>186</td>\n",
       "      <td>20170330</td>\n",
       "      <td>FEMALE</td>\n",
       "      <td>필수 단계</td>\n",
       "      <td>한글</td>\n",
       "      <td>가나다 익히기</td>\n",
       "      <td>NONE</td>\n",
       "      <td>1</td>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>10</td>\n",
       "      <td>2022-03-18 14:29:10</td>\n",
       "      <td>17</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>1</td>\n",
       "      <td>자음 이해</td>\n",
       "      <td>이해력</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>37192</th>\n",
       "      <td>37193</td>\n",
       "      <td>186</td>\n",
       "      <td>20170330</td>\n",
       "      <td>FEMALE</td>\n",
       "      <td>필수 단계</td>\n",
       "      <td>한글</td>\n",
       "      <td>가나다 익히기</td>\n",
       "      <td>NONE</td>\n",
       "      <td>1</td>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>10</td>\n",
       "      <td>2022-03-18 15:20:51</td>\n",
       "      <td>7</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>1</td>\n",
       "      <td>자음 이해</td>\n",
       "      <td>이해력</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>37282</th>\n",
       "      <td>37283</td>\n",
       "      <td>186</td>\n",
       "      <td>20170330</td>\n",
       "      <td>FEMALE</td>\n",
       "      <td>필수 단계</td>\n",
       "      <td>한글</td>\n",
       "      <td>가나다 익히기</td>\n",
       "      <td>NONE</td>\n",
       "      <td>1</td>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>10</td>\n",
       "      <td>2022-03-18 15:31:17</td>\n",
       "      <td>7</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>ㄴ</td>\n",
       "      <td>0</td>\n",
       "      <td>자음 이해</td>\n",
       "      <td>이해력</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>37283</th>\n",
       "      <td>37284</td>\n",
       "      <td>186</td>\n",
       "      <td>20170330</td>\n",
       "      <td>FEMALE</td>\n",
       "      <td>필수 단계</td>\n",
       "      <td>한글</td>\n",
       "      <td>가나다 익히기</td>\n",
       "      <td>NONE</td>\n",
       "      <td>1</td>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>10</td>\n",
       "      <td>2022-03-18 15:31:25</td>\n",
       "      <td>7</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>1</td>\n",
       "      <td>자음 이해</td>\n",
       "      <td>이해력</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>39804</th>\n",
       "      <td>39805</td>\n",
       "      <td>191</td>\n",
       "      <td>20170723</td>\n",
       "      <td>FEMALE</td>\n",
       "      <td>필수 단계</td>\n",
       "      <td>한글</td>\n",
       "      <td>가나다 익히기</td>\n",
       "      <td>NONE</td>\n",
       "      <td>1</td>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>10</td>\n",
       "      <td>2022-03-22 15:51:01</td>\n",
       "      <td>7</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>ㄹ</td>\n",
       "      <td>1</td>\n",
       "      <td>자음 이해</td>\n",
       "      <td>이해력</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>157 rows × 19 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "         시퀀스  아이 고유 식별 값   아이 생년월일   아이 성별     단계 컨텐츠 분류1  컨텐츠 분류2 컨텐츠 분류3  \\\n",
       "695      696         129  20180310    MALE  필수 단계      한글  가나다 익히기    NONE   \n",
       "775      776         128  20170804  FEMALE  필수 단계      한글  가나다 익히기    NONE   \n",
       "800      801         128  20170804  FEMALE  필수 단계      한글  가나다 익히기    NONE   \n",
       "821      822         128  20170804  FEMALE  필수 단계      한글  가나다 익히기    NONE   \n",
       "845      846         128  20170804  FEMALE  필수 단계      한글  가나다 익히기    NONE   \n",
       "...      ...         ...       ...     ...    ...     ...      ...     ...   \n",
       "36948  36949         186  20170330  FEMALE  필수 단계      한글  가나다 익히기    NONE   \n",
       "37192  37193         186  20170330  FEMALE  필수 단계      한글  가나다 익히기    NONE   \n",
       "37282  37283         186  20170330  FEMALE  필수 단계      한글  가나다 익히기    NONE   \n",
       "37283  37284         186  20170330  FEMALE  필수 단계      한글  가나다 익히기    NONE   \n",
       "39804  39805         191  20170723  FEMALE  필수 단계      한글  가나다 익히기    NONE   \n",
       "\n",
       "       단계.1  단계별 문제 번호  문제 세부 번호  문제 고유 식별 값                학습 시각  문제풀이 소요시간  \\\n",
       "695       1          4         1          10  2021-12-31 17:57:13          8   \n",
       "775       1          4         1          10  2021-12-31 21:52:37          5   \n",
       "800       1          4         1          10       22-1-1 9:11:11          5   \n",
       "821       1          4         1          10       22-1-1 9:16:06         10   \n",
       "845       1          4         1          10       22-1-1 9:22:08         12   \n",
       "...     ...        ...       ...         ...                  ...        ...   \n",
       "36948     1          4         1          10  2022-03-18 14:29:10         17   \n",
       "37192     1          4         1          10  2022-03-18 15:20:51          7   \n",
       "37282     1          4         1          10  2022-03-18 15:31:17          7   \n",
       "37283     1          4         1          10  2022-03-18 15:31:25          7   \n",
       "39804     1          4         1          10  2022-03-22 15:51:01          7   \n",
       "\n",
       "      문제 정답 아이 블록 입력 데이터  정오답 통계 메인 키 향상 능력  \n",
       "695       ㄹ            ㄹ    1   자음 이해   이해력  \n",
       "775       ㄹ            ㄹ    1   자음 이해   이해력  \n",
       "800       ㄹ            ㄹ    1   자음 이해   이해력  \n",
       "821       ㄹ            ㄹ    1   자음 이해   이해력  \n",
       "845       ㄹ            ㄹ    1   자음 이해   이해력  \n",
       "...     ...          ...  ...     ...   ...  \n",
       "36948     ㄹ            ㄹ    1   자음 이해   이해력  \n",
       "37192     ㄹ            ㄹ    1   자음 이해   이해력  \n",
       "37282     ㄹ            ㄴ    0   자음 이해   이해력  \n",
       "37283     ㄹ            ㄹ    1   자음 이해   이해력  \n",
       "39804     ㄹ            ㄹ    1   자음 이해   이해력  \n",
       "\n",
       "[157 rows x 19 columns]"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "pledo_rm[pledo['문제 고유 식별 값'] == 10]"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
