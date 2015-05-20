Title: Intro to CRDT's
Date: 2015-5-20 10:20
Tags: CRDT

To begin to understand Conflict-free Replicated Data Types it would be good to first understand why it is that you even need them in the first place and what problem they solve.

Distributed systems are hard. However understanding your distributed computing problem and the compromises you must make go a long way to conquering whatever project that you are tackling. By asking the right questions you can better understand what it is you are giving up and gaining when you do start making decisions about your project.

We will ask a rather simple question to get a good understanding the problem area:

> In a world plagued by uncertainty, what is truth?

For a non distributed system this is rather easy: truth is whatever your database returns as the answer. You simply query the single source of truth and it responds with the what you are looking for, however it overlooks the uncertainty part of the question. This non distributed system chooses to take the problem of uncertainty and build a monolith. What is wrong with this approach is that eventually the monolith will be crushed by it's own weight. Most of the time the monolith solution is the correct answer to this question but if you want to build a system that is incredibly large you can not just keep stacking chairs on top of each other and expect to arrive at the moon.

What happens when you do not want to build a monolith? One approach is to take the idea of single point of truth and apply it too a distributed system. You can take a cluster of computers and make them use Paxos or two-phase-commit to agree upon an ordering of received transactions then then calculate a truth that all the members of the cluster share. This leads to a truth that has a property called strong consistency, at any point in time all the clusters will share a consistent truth if they meet certain conditions. The devil is in the details. This strong consistency comes at the cost of being very expensive and only available to certain types of distributed systems. While your truth will always be perfect you may not be able to access it at any point in time and you may not be able to write to it whenever you feel like it. You may need to know certain things about your distributed system, like how many computers are in your cluster, which in some systems is impossible to tell. And there may be some cases where the semantics of your data type may lead to data being lost in the case of concurrent updates. What you may want to do is change what your definition of truth is in a distributed system.

This leads to what is called weak consistency. Instead of electing a leader and recreating the problems of a single point of truth in a system you just give up on that and make truth be eventually consistent. If you make your construct your truth in such a way that additions (and if you are really careful removals) to it regardless of received order result in a stabilized state you can get rid of the need to have a single ledger that dictates the order of events. This type of truth is called a Conflict-free Replicated Data Type and it may just be the answer to your problem.

The way it gets to a stable state is by the careful application of mathematical properties. The CRDT must fulfill three properties. If you have truth that can be modified at two places at the same time and once combined result in the same truth. You may remember this from math class, it is called communicative property:
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

Luckily for you these are already well known properties in mathematics and together they are called