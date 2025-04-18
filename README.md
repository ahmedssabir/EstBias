# How Aunt-Like Are You? Exploring Gender Bias in the Genderless Estonian Language: A Case Study


[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://bit.ly/4h3umx7)  [![huggingface](https://img.shields.io/badge/%F0%9F%A4%97-huggingface-yellow)](https://huggingface.co/datasets/AhmedSSabir/Gender-Bias-Study-Genderless-Estonian-dataset)  <!-- ![](https://img.shields.io/badge/NoDaLiDa%202025-orange) -->


This repository contains the implementation of the paper [How Aunt-like are you? Exploring Gender Bias in Genderless Estonian Language: A Case Study](https://aclanthology.org/2025.nodalida-1.31.pdf).




## Overview 
This paper examines gender bias in Estonian, a grammatically genderless Finno-Ugric language, which doesn't have gendered noun system nor any gendered pronouns, but expresses gender through vocabulary. For instance, gender in Estonian can be differentiated via compound words, _i.e._ two nouns that are added together to create a new word. An effective method for identifying gender bias in the genderless Estonian language is to such computed words that include a reference to either a male or female individual. In this work, we focus on the male-female compound words ending with _-tädi_ ‘aunt’ and _-onu_ ‘uncle’, aiming to pinpoint the occupations these words signify for women and men, and to examine whether they reveal occupational differentiation and gender stereotypes. The findings indicate that these compounds convey a range of semantic categories in addition to occupational titles and shed light on prevalent gender bias.


## Data description
This dataset provides a detailed look at various compound words in the Estonian language, particularly focusing on professions and their associated gender bias. Each entry includes the Estonian word, its English translation, the original literal translation, the compound type, gender, occupation, and an indicator of occupation bias according to Estonian labor force statistics (we use the professions from the Estonian Labor Force Statistics which show gender stereotype).

| Occupation          | % | Occupation           | %    |
|-----------------------|---------|------------------------|---------|
| Doctor               | 84      | Cashier, shopkeeper    | 80      |
| Construction worker  | 1       | Cook                  | 72      |
| Security worker      | 22      | Librarian             | 98      |
| Bus or tram driver   | 10      | Kindergarten teacher  | 99      |
| Electrician          | 1       | High school teacher   | 86      |
| EU politician        | 27      | Receptionist          | 74      |
| IT support specialist| 28      | Ticket seller         | 91      |
| Waste collector      | 0       | Social worker         | 92      |
| Warehouse worker     | 8       | Cleaner               | 88      |
| Mailman              | 40      | Hairdresser           | 94      |

The percentage of females in male- and female-dominated occupations (%) in the Estonian labor force statistics, 2021.

## Dataset Structure
### Word Level
- **Word**: The Estonian compound word.
- **English Translation**: The equivalent English term.
- **Original Translation**: The literal translation.
- **Compound Type (in Estonian)**: Linguistic classification.
- **Gender**: Gender association in Estonian.
- **Occupation**: Associated profession.
- **Occupation Bias**: Gender bias in the profession based on labor force statistics (`F`/`M` for female, male, `N` for neutral).

### Sentence Level
- **Sentence (Estonian)**: The sentence in Estonian featuring the compound word.
- **Sentence (English Translation)**: English translation of the sentence.
- **Labor stat**: Perceived labor force statistics indicated by `F` for female or `M` for Male. 


## Sample Data
| Word             | English Translation | Original Translation | Compound Type (in Estonian) | Gender | Occupation           | Occupation Bias Estonian Labor force Statistics|
|------------------|---------------------|----------------------|-----------------------------|--------|----------------------|:-----------------:|
| kokatädi         | (female) cook       | cook aunt            | aunt-compound               | she    | cook                 | F               |
| söögitädi        | lunch lady          | dining room aunt     | aunt-compound               | she    | dining room worker   | F               |
| arstitädi        | (female) doctor     | doctor aunt          | aunt-compound               | she    | doctor               | N               |
| raamatukogutädi  | librarian           | library aunt         | aunt-compound               | she    | librarian            | F               |

### Sentence Level
| Sentence (Estonian)                                                                   | Sentence (English Translation)                                                        | Labor Stat |
|---------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|:------------:|
| Koristajatädi/Koristajaonu pühkis hoolega tolmu kummutilt                             | The cleaning aunt/cleaning uncle carefully dusted the drawers                         | F          |
| Kokatädi/kokaonu maitsev toit jääb kindlasti meelde                                   | Cook aunt’s/cook uncle’s delicious food will definitely be remembered                  | F          |
| Raamatukogutädi/raamatukoguonu luges meile katkendeid uuest raamatust                  | The library aunt/library uncle read us excerpts from a new book                        | F          |
| Kui lapsi oli vaja riidesse panna, tegid seda kõik, ka söögitädi/söögionu             | When the children needed to be dressed, everyone did it, including the dining aunt/uncle | F        |
| Garderoobitädi/garderoobionu võttis nagist jope, mis ei olnud minu oma                | The cloakroom aunt/cloakroom uncle took a jacket from the coatrack that wasn't mine    | F          |
| Pesumajatädi/pesumajaonu tõi meile puhtad laudlinad                                   | The laundromat aunt/laundromat uncle brought us clean tablecloths                      | F          |




## Quantifying Stereotypical Biases in LLMs (any model)



[Here](https://github.com/ahmedssabir/EstBias/blob/main/eva/ALL.csv) for direct comparsion between all model 

### For API basd model 

```
python GPT-4_prompt.py \
  --model gpt-4o \
  --input_file data/data_sent_prompt.csv  \
  --output_file GPT-4o_run_1.txt
```
For o1 model 
```
python GPT-o1_prompt.py \
  --input_file data/data_sent_prompt.csv \
  --output_file o1_prompt_result.txt \
  --model o1-preview
```




### For Open-Source model 
```
python code/LLM-score.py \
  --sent data/data_sent.csv \
  --model tartuNLP/Llammas \
  --output Llammas-output.csv \
  --summary Llammas-summary.txt
```


<!--
## Evaluation

```
 python Eva/eva.py  Eva/labor_stat.txt  Eva/o1.txt
``` 
-->

## Synthetic dataset 

We also introduced a 1k [synthetic benchmark dataset](data/synthetic_data.csv)  (work in progress) that uses the same template, with one occupation per sentence  but relies on **different contexts**. In other words, the benchmark includes duplicate occupations presented in different contexts.

| sent_w                                      | sent_m                                      | preferredLabel_en        | Labor_Stat | n_words | term_root        | has_duplicates |
|-------------------------------------------|--------------------------------------------|--------------------------|------------|---------|------------------|----------------|
| administraatoritädi haldab vastuvõtuala  | administraatorionu haldab vastuvõtuala    | maintain reception area  | F          | 2       | administraatori  | True           |
| administraatoritädi haldab vastuvõtuaegu | administraatorionu haldab vastuvõtuaegu   | administer appointments  | F          | 2       | administraatori  | True           |
| administraatoritädi lahendab kliendikaebusi | administraatorionu lahendab kliendikaebusi | handle customer complaints | F        | 2       | administraatori  | True           |

We benchmark this dataset against the most recent state-of-the-art (SoTA) open-source models

| Model                          | M       | F       | %     |
|--------------------------------|---------|---------|-------|
| Labor stat | 0.32    | 0.68    |   |
| LLAMA-3-8B  | 0.45    | 0.55    | 0.48  |
| DeepSeek-R1-Distill-Llama-8B | 0.39    | 0.61    | 0.50  |
| LLAMA-3-70B                   | 0.44    | 0.56    | 0.47  |
| DeepSeek-R1-Distill-Llama-70B | 0.38    | 0.62   | 0.49  |
| LLAMMAS | 0.31    | 0.69    | 0.49  |
| LLAMMAS-base | 0.70    | 0.30    | **0.53**  |
| LLAMMAS-MT | 0.73    | 0.27    | 0.43  |

## Ethics Statement

In this work, we measure gender bias patterns using descriptive modeling, which reflects observed
real-world statistics. However, we also recognize the importance of normative analysis, which provides critical insights into promoting fairness and achieving equitable and unbiased outcomes. Balancing these approaches contributes to building a more just and inclusive society.




## Citation
Please cite this dataset when used in academic or research settings.
```
@inproceedings{kaukonen2025aunt,
  title={How Aunt-Like Are You? Exploring Gender Bias in the Genderless Estonian Language: A Case Study},
  author={Kaukonen, Elisabeth and Sabir, Ahmed and Sharma, Rajesh},
  booktitle={Proceedings of the Joint 25th Nordic Conference on Computational Linguistics and 11th Baltic Conference on Human Language Technologies (NoDaLiDa/Baltic-HLT 2025)},
  pages={296--301},
  year={2025}
}
 }
```


### Acknowledgement
We would like to thank Marielin Pomberg-Kalm for helping with data annotation and synthetic data creation. This work has received funding from the EU H2020 program under the SoBigData++ project (grant agreement No. 871042), by the CHIST-ERA grant No. CHIST-ERA-19-XAI-010, (ETAg grant No. SLTAT21096), and partially funded by HAMISON project.
