title: Intro to CRDT's
Date: 2015-5-20 10:20
Tags: CRDT

To begin to understand Conflict-free Replicated Data Types it would be good to first understand why it is that we even need them in the first place and what problem they solve.

Distributed systems are hard. However understanding your distributed computing problem and the compromises you must make go a long way to conquering whatever project that you are tackling. By asking the right questions you can better understand what it is you are giving up and gaining when you do start making decisions about your project.

We will ask a rather simple question to get a good understanding the problem area:

> In a world plagued by uncertainty, what is truth?

For a non distributed system this is rather easy: truth is whatever your database returns as the answer. You simply query the single source of truth and it responds with the what you are looking for, however it overlooks the uncertainty part of the question. This non distributed system chooses to take the problem of uncertainty and build a monolith. What is wrong with this approach is that eventually the monolith will be crushed by it's own weight. Most of the time the monolith solution is the correct answer to this question but if you want to build a system that is incredibly large you can not just keep stacking chairs on top of each other and expect to arrive at the moon.

The next answer to the problem is just a turning the non distributed system on it's ear and getting the single source of truth in a distributed 