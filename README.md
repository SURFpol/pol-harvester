Project Open Leermaterialen Harvester
=====================================

A repo meant to scrape and extract education materials.

Installation
------------

Install and activate requirements with:

```bash
conda create --copy -f environment.yml
source activate surf-harvest
```

The harvester depends on Django, mostly to be able to work with a database. 
With a database its easier to track which steps of the harvest failed 
and to store all kinds of meta data from the harvesting process.
It's easier to search a database for error information and that already proved useful during debugging.
One thing that Django provides is an administration interface that lets you inspect harvested objects in a breeze.

To setup Django:

```bash
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```    

Now you should be able to login with your credentials at:

```bash
http://localhost:8000/admin/
```

Datagrowth
----------

Datagrowth is a set of open source tools that helps to gather and organise data through Django.
I've included the sources to this repo directly, but I mostly copy pasted it from another repo.
When Datagrowth gets released as a package we should consider installing it as a dependency 
rather than using the copied sources.

Harvesting the harvester
------------------------

Our first objective was to harvest Edurep another harvester. 
I've made some management commands that harvest Edurep step by step.

#### 1.) Downloading data

There are a few ways to get data from Edurep
- As a XML data dump (the standard dump from Kennisnet)
- As a JSON dump (generated by code from Jelmer)
- As a search query

If you got the data as a dump proceed to step 2. If you only have a Edurep query you can download the data with:

```bash
./manage.py harvest_edurep_api --query <your-query>
```

#### 2.) Extracting relevant data

Edurep contains a lot of data. However it is often not in a nice format and we probably don't need everything.
That's why we're going to extract and format the data. How this is done depends slightly on your initial source.
Use one of the commands below:

```bash
# When reading XML dumps
./manage.py extract_edurep_dir --input <the-XML-dump-directory> --output <your-data-file>

# When reading JSON dumps
./manage.py extract_edurep_json --input <the-JSON-dump-file> --output <your-data-file>

# When using search queries
./manage.py extract_edurep_api --query <your-query> --output <your-data-file>
```

Notice how all these commands create a similar output file that we'll call the ```data file``` from now on.

#### 3.A) Download content

Edurep only harvests meta data. To get the content of the learning materials you can run the following commands.
These commands internally use TIKA to extract texts from files.

```bash
./manage.py download_edurep --input <data-file>
./manage.py extract_text_edurep_files --input <data-file> --formats application/msword,application/octet-stream,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,vnd.openxmlformats-officedocument.presentationml.presentation
```

This will put the content in files on your harddisk under the ```media``` directory. 
You can find all downloaded content with paths as well as metadata from Tika in the database.

#### 3.B) Download and transcribe video

Some of the Edurep content consists of video. We need to download this content separately using the commands below.
Internally these commands use YoutubeDL and Kaldi to download the audio and transcribe to text.

```bash
./manage.py download_edurep_video --input <data-file>
./manage.py transcribe_edurep_video --input <data-file>
```

As with step 3.A all files will be stored under ```media``` while the paths to these files 
and possible error messages that occured will reside in the database.
Note that only .wav files get stored permanently.


#### 3.C) Download and extract IMS Content Packages

Other content consists of content packages as defined by IMS.
You can download and extract these with the following commands:

```bash
./manage.py download_edurep_imscp --input <data-file>
./manage.py extract_text_edurep_imscp --input <data-file>
```

This places the package download and extracted files under ```media```. It will also process the extracted files with Tika.
Errors in this process are to be ofund in the database.

#### 4.) Export data and profit!

There is no use in having data if you can't use it somewhere else like in Elastic Search.
To be able to do that simply run the following command:

```bash
./manage.py dump_edurep --input <data-file> --output <your-output-directory>
```

This dump does two things:
1. It places all objects in files and assigns a unique id to these objects, which is then used as the filename.
2. It places all objects with texts together in a file called with_text.json.

For export of WUR data it works slightly different.
This data is already formatted in a format close to the required format.
To make the format completely compatible we just need to rewrite it slightly by running:

```bash
./manage.py reformat_dump --input <wur-json-file> --output <your-output-directory>
```
