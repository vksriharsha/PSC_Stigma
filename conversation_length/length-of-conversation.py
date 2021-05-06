
import pandas as pd

posts = pd.read_csv("G:/Tim/Documents/homework/ds401/sql/reddit_posts_dryalcoholics_clean.csv")
comments = pd.read_csv("G:/Tim/Documents/homework/ds401/sql/reddit_comments_dryalcoholics_clean.csv")
addictionary = pd.read_excel("G:/Tim/Documents/homework/ds401/addictionary.xlsx")
print(posts.head())
print(comments.head())
print(addictionary.head())

postSort = posts.sort_values(by="name")
comSort = comments.sort_values(by="link_id")
print(postSort.head())
print(comSort.head())

print(addictionary.loc[0,'Word'].lower())


convos = pd.DataFrame(columns = ['link_id', 'title', 'self_text', 'num_comments', 'contains_stigma','stigma_alert','comment_word_count', 'comment_character_count', 'deleted_comments', 'blank_comments', 'afinn_score', 'afinn_words_scored'])
pos = 0
total = 0


print(comSort.iloc[1000,0])
split = comSort.iloc[1000,0].split()
for i in range(0, len(split)):
    print(split[i] + " " + str(len(split[i])))
#print(len(split))

for i in range(0,len(postSort.index)):
    test = postSort.iloc[i,5]
    count = 0
    comment_word_count = 0
    comment_char_count = 0
    deleted = 0
    blank = 0
    stigma = False
    s_alert = False
    afinn_score = 0
    words_scored = 0
    for j in range(0, len(addictionary.index)):
        if j != 159 and addictionary.loc[j,'Word'].lower() in postSort.iloc[i,1]:
            stigma = True
            if not pd.isna(addictionary.loc[j,'Type']):
                s_alert = True
        if j != 159 and not pd.isna(postSort.iloc[i,2]) and addictionary.loc[j,'Word'].lower() in postSort.iloc[i,2]:
            stigma = True
            if not pd.isna(addictionary.loc[j,'Type']):
                s_alert = True
    while pos < len(comSort.index) and test > comSort.iloc[pos,3]:
        pos+=1
    while pos < len(comSort.index) and test == comSort.iloc[pos,3]:
        count+=1
        pos+=1
        total+=1
        afinn_score = afinn_score + comSort.iloc[pos,8]
        words_scored = words_scored + comSort.iloc[pos,9]
        #print(comSort.iloc[pos,0])
        if pd.isna(comSort.iloc[pos,0] or comSort.iloc[pos,0].isspace()):
            blank+=1
        elif comSort.iloc[pos,0] == ' deleted ' or comSort.iloc[pos,0] == ' removed ':
            deleted+=1
        else:
            split = comSort.iloc[pos,0].split()
            comment_word_count = comment_word_count + len(split)
            for k in range(0, len(split)):
                comment_char_count = comment_char_count + len(split[k])
    print(test + ": " + str(count))
    convos.loc[i] = [postSort.iloc[i,5], postSort.iloc[i,1], postSort.iloc[i,2], count, stigma, s_alert, comment_word_count, comment_char_count, deleted, blank, afinn_score, words_scored]
    #convos.append({'link_id': postSort.iloc[i,5], 'title': postSort.iloc[i,1], 'self_text': postSort.iloc[i,2], 'num_comments': count},
    #ignore_index=True)
print("Done")
print(total)
convos.to_csv('G:/Tim/Documents/homework/ds401/sql/dryalcoholics_output.csv')

