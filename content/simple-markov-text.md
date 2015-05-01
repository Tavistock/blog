Title: Markov Poem
Date: 2015-4-7 10:20
Tags: clojure, java

I had an assignment to make a poem generator for my computer science class but it involved arrays and random choice. I thought I could do a little bit better so I made a markov chain text generator.

You've probably seen a markov text generator before because everyone and their mother has some gimmick twitter trained off of a humorous combo like [a philosopher and a celebrity](https://twitter.com/kimkierkegaard) or [drugs and spam](https://twitter.com/erowidrecruiter). Mine is going to be a bit simpler.

### Data Munging
First we need to get the data that we are going to train the markov chain off of. I am going to just use flat .txt files that I find on the internet as models for my poems. The data structure I need is a sequential list of strings because the simple markov chain I'm making just needs to know the word it wants and the word after for it's state machine. This doesn't make sense yet but hold on.

Data munging sounds a bit dirty and urban dictionary seems to think it has something to do with sex however it is simply getting the data we want in the proper format that we want. What I did here was make a simple open url and open file that make a text blobs (without new lines) then make a list of words. The only real reason I'm mentioning this is because when getting the text blob into a list of words I used the powerful and often untaught [Stream API](https://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html) in the Java.util standard library. If you are familiar with functional programming this API can make your code more succinct while keeping different concerns separate.
``` java
public static List<String> process (String text){
    return Stream.of(text.split("\\W"))
            .filter((x) -> (! x.equals("")))
            .collect(Collectors.toList());
}
```
As you can read I make a stream out of the text blob split on whitespace characters, then filter it for any empty strings, and finally collect (parallel reduce as far as I can tell) it as a list.

### Markov Through Structure (aka Data > Functions > Macros)
This is where I'm going to throw a lot of information at you. Markov chains can be though of as little machines that make choices. You get into a state and then from that state you transition into another state. This seems like a good way of modeling games or something but it doesn't seem like a good way of making sentences or poems. If you think a little bit obtusely it will all begin to make sense. Make the current word the state and then all words that appear after that word as it's choices. What you can do with this is randomly move from state to choice and then make the next choice the new state. It may not make meaningful sentences(it might make interesting sentences sporadically) but it will make sentences that are more coherent than a pure random approach.

What we want to do is make our list of words into a data structure that relates state to choices. Luckily this is a rather common problem(trust me you want rather common problems) so there is a solution in Java and pretty much every oter programming language. It is called a HashMap(Dict in python, Map or {} literal in clojure) and I am going to use it to map from a String to a LinkedList of Strings. A saying in Clojure is that data is better than functions is better than macros and here where we could make each state machine a function that chooses a choice it is easier to make a Map that points to choices.
Heres the code:
``` java
public static HashMap<String, LinkedList<String>> getDict(List<String> chain) {
    String last = "";
    HashMap<String, LinkedList<String>> dict = new HashMap();
    for (String word: chain){
        if (!"".equals(last)) {
            if (dict.get(last) == null) {
                LinkedList<String> val = new LinkedList();
                val.push(word);
                dict.put(last, val);
            } else {
                LinkedList<String> val = dict.get(last);
                val.push(word);
            }
        }
        last = word;
    }

    return dict;
}
```
We take the list and for each of the Strings in the list we add it as a key in the hash map and add the word after it as a new linked list or puch it onto the pre-existing linked list. This is bad in my opinion because we mutate the list when we add to it rather than returning a new list and this can lead to problems when we introduce multi-threading but I have no plans of multi-threading this so whatever. If we are at the first entry in a linked list we can't do anything because we need the last word so we assign the current word as the last word and do nothing else.

### Running this Infernal Machine
Next we need to run this markov chain and we are going to use a random number generator as our engine. What we do is randomly choose a key from the Map(which doesn't support this so we just make a list out of keys and select from that) then randomly choose a string out of the LinkedList and make that the new key for the map until our result list is the length we want it to be:
``` java
public static String randMarkov(HashMap<String, LinkedList<String>> map,
                                 Integer size) {
    String result = "";
    List<String> keysAsArray = new LinkedList<>(map.keySet());
    Random r = new Random();
    String key = keysAsArray.get(r.nextInt(keysAsArray.size()));

    result = result.concat(key);
    while (result.length() <= size) {
        List<String> list = map.get(key);
        String next = list.get(r.nextInt(list.size()));
        result = result.concat(" " + next);
        key = next;
    }

    return result;
}
```

### Putting it All Together
Seeing as how I made my API out of normal functions I just sort of stitch them together to get them to do what I want:
``` java
public static void main(String[] args){
    String address = "https://raw.githubusercontent.com" +
            "/lspector/clojinc/master/Jabberwocky.txt";
    System.out.println(randMarkov(getDict(process(getURL(address))),140));
}
```
This would look a lot better if I made a thread and thrush function in Java like I have in Clojure:
```clojure
(def address
"https://raw.githubusercontent.com/lspector/clojinc/master/Jabberwocky.txt")

(-> address (getUrl) (process) (getDict) (randMarkov 140))
```

I made a getURL and getFile command that just get the text blob from the file system or from the internet.

