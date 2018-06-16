# MyUni Downloader 

So you want all the lecture notes and previous exams from MyUni. Well this little script may help you!

## What is does!

Logs into the course course page at [myuni.adelaide.edu](https://myuni.adelaide.edu.au) and downloads all the files from the modules page (or just the pdfs).

## Get started

1. install python, pip
2. `pip install robobrowser`
3. `git clone this`

## Usage

```
python myuni-dl.py --username a1111111 --password 'pa$$$$$$$' --course 36284
```

![example of the course number](https://i.imgur.com/tx1lq8M.png)
`^^` Myuni course number

## Basic Behaviour

1. Logs into myuni
2. Finds all module links
3. Goes through each link downloads the file

## Additional Behaviour

4. Download only specific file types eg: `--downloadOnly pdf`
5. Check if the file has already been downloaded (if the script was interrupted)