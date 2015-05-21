Title: Intro to CRDTs
Date: 2015-5-20 10:20
Tags: CRDT

To begin to understand Conflict-free Replicated Data Types it would be good to first understand why it is that you even need them in the first place and what problem they solve.

Distributed systems are hard. However understanding your distributed computing problem and the compromises you must make go a long way to conquering whatever project that you are tackling. By asking the right questions you can better understand what it is you are giving up and gaining when you do start making decisions about your project.

We will ask a rather simple question to get a good understanding the problem area:

> In a world plagued by uncertainty, what is truth?

Deny Uncertainty
---
For a non distributed system this is rather easy: truth is whatever your database returns as the answer. You simply query the single source of truth and it responds with the what you are looking for, however it overlooks the uncertainty part of the question. This non distributed system chooses to take the problem of uncertainty and build a monolith. What is wrong with this approach is that eventually the monolith will be crushed by it's own weight. Most of the time the monolith solution is the correct answer to this question but if you want to build a system that is incredibly large you can not just keep stacking chairs on top of each other and expect to arrive at the moon.

Coordinate through Uncertainty
---
What happens when you do not want to build a monolith? One approach is to take the idea of single point of truth and apply it too a distributed system. You can take a cluster of computers and make them use Paxos or two-phase-commit to agree upon an ordering of received transactions then then calculate a truth that all the members of the cluster share. This leads to a truth that has a property called strong consistency, at any point in time all the clusters will share a consistent truth if they meet certain conditions. The devil is in the details. This strong consistency comes at the cost of being very expensive and only available to certain types of distributed systems. While your truth will always be perfect you may not be able to access it at any point in time and you may not be able to write to it whenever you feel like it. You may need to know certain things about your distributed system, like how many computers are in your cluster, which in some systems is impossible to tell. And there may be some cases where the semantics of your data type may lead to data being lost in the case of concurrent updates. What you may want to do is change what your definition of truth is in a distributed system.

Embrace Uncertainty
---
This leads to what is called weak consistency. Instead of electing a leader and recreating the problems of a single point of truth in a system you just give up on that and make truth be eventually consistent. If you make your construct your truth in such a way that additions (and if you are really careful removals) to it regardless of received order result in a stabilized state you can get rid of the need to have a single ledger that dictates the order of events. This type of truth is called a Conflict-free Replicated Data Type and it may just be the answer to your problem.

Three's Company
---
The way it gets to a stable state is by the careful application of mathematical properties. The CRDT must fulfill three properties. If you have truth that can be modified at two places at the same time that once combined result in the same truth you do not need to coordinate. You may remember this from math class, it is called communicative property:
```
Communicative => (+ a b) = (+ b a)
```
The next property is one of total ordering so we do not need a ledger of transactions. Transitioning into a stable state will be guaranteed no matter what order you receive the changes to our truth in. This is called the associative property:
```
Associative => (+ a (+ b c)) = (+ (+ a b) c)
```
The final one is called the idempotent property. When performing an operation multiple times it will result in the same state. With this you can receive operations on our truth twice and end up in same state which happens pretty often in distributed programming because of message duplication:
```
Idempotent => (+ a a) = a
```

Semi-Lattices
---
Luckily for you these are already well known properties in mathematics and together they make up (upper or lower bound) semi-lattices. An example of a semi-lattice is `max` on two integers or `union` on two sets. When given a list of integers when `max` is applied from any starting point (communicative property), on any random order of integers (associative property), and any number of duplicate integers (idempotent property) you will always get the correct `max` for that list of integers:
```
find the max of: [8 9 5 7 1]

        list w/ dupes := 8 9 5 7 1 9        list random order := 5 9 7 1 8
                         \ / \ / \ /                             \ / \ / |
max =>                    9   7   9                               9   7  8
                           \ /  /                                  \ /  /
max =>                      9  9                                    9  8
                             \/                                      \/
max =>                        9                                       9
``` 
A same thing applies to sets using the `union` operation.

A Bad Example
---
But you run into a problem using this as the only basis for creating useful CRDTs. As an example you could construct, merely as an example,  a CRDT that we will call bad-Last-Write-Wins or `bad-LWW` that forms a semi-lattice but loses useful bits of your information. For this `bad-LWW` we will make the semi-lattice keep the data of the highest wall-clock time-stamp and the operation will be called `recent`. Now assuming all the wall-clocks are in sync (which is an impossible assumption for a number of reasons*) whenever we call `recent` on two `bad-LWW` it will choose the latest. No matter the order a computer in a cluster receives `bad-LWW`s and then calls `recent` on them it will reach the same truth. If it gets duplicates of the same `bad-LWW` it will always reach the same state.

For this demonstration a `bad-LWW` data structure is a tuple of `[time-stamp data]` where the time-stamp is an integer n for the seconds after initialization and data is arbitrary data. The operation on the `bad-LWW`, `recent`, just returns the highest time-stamped tuple. As a diagram like the integers and `max` operation it looks like:
```
find the most recent of:
             [8 "acd"] [9 "acde"] [5 "ab"] [7 "ac"] [1 "a"]
                 \         /          \      /        |
recent =>         [9 "acde"]         [7 "ac"]     [1 "a"]
                      \            /            /
recent =>               [9 "acde"]      [1 "a"]
                              \          /
recent =>                      [9 "acde"]
```

Needs Improvement
---
Now this `bad-LWW` is called this because it does not preserve the semantics of the underlying data structure (it looks like time-stamps 5 and 7 happened concurrently and a bit of truth was lost from the string because of that) nor is the wall-clock time-stamp a viable strategy in a real world system. Now with this simple yet useless CRDT you can further refine it until it is something that is more valuable for real world problems. In the next few blog posts I will talk at first about the different species of known CRDT, then focus on ways of representing sequences in distributed computing, and finally do a deep dive on the implementation of LSEQ, a data structure for representing sequences, in clojure.