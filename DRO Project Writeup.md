
# Modifying A DRO for Hardware Regression Testing

Over the past few months at works we've been making slight adjustments to our device such as how we manufacture certain components or the duration of certain steps in the protocol. Due to the sensitive nature of our protocols on the biological side this led us to ask the very reasonable question: Do the knew devices behave the same as the old ones? One way to go about obtaining that answer would be to run a myriad of biological experiments A/B testing the different devices to see if these various hardware changes had any impact on the downstream biological results. While that is definitely still in the cards for a long term solution, biological tests are very expensive and time consuming so something to provide initial reassurance was very valuable. That's the motivation for this project. 

The basic idea behind the project is to take an off the shelf (and cheap) Digital Read Out (DRO) meant to be used for hobbyist machining and other shop tasks, and re-purpose it to measure the motion of the syringe pumps in our devices. As this project was mainly a proof of concept I decided on the cheapest DRO I could find on amazon that also included a detachable USB cable. This [Shahe DRO](https://www.amazon.com/Digital-Readout-0-150mm-Accurate-Machines/dp/B089ZSG84J/ref=sr_1_3?crid=1W2C2KIMURKP8&keywords=shahe%2Bdro&qid=1678823611&sprefix=shahe%2Bdro%2Caps%2C77&sr=8-3&th=1) was the winner. 

![Shahe DRO Product image](https://m.media-amazon.com/images/I/61Ycdt+-f2L._SL1300_.jpg)

As I began looking for similar project to get started I stumbled upon an invaluable resource. [Touch DRO](https://www.touchdro.com/resources/adapters/diy/) is a really cool looking project that aims to take cheap off the shelf DROs such as the Shahe model I was using and provide a much more highly functioning app with full 3-axis control. While I didn't need all the bells and whistles included in the full version in this single axis project, I would be remiss if I didn't give that particular project a shout out as he did a lot of the work that got  me moving in the right direction. This article [Shahe Linear DRO Scales](https://www.touchdro.com/resources/scales/capacitive/shahe-dro-scales.html) was particularly useful to me. In it the author describes the communication protocol of the DRO. That data format is called BIN6 and is commonly used in digital calipers. 

From there I set out to learn more about this BIN6 data format. Luckily for me searching around for similar projects I found the second incredibly useful article of this project. [300 mm DRO with Arduino (ATTiny85 and Nano)](https://curiousscientist.tech/blog/300-mm-dro-with-arduino) from the "Curious Scientist" blog basically got me the rest of the way there. For reference these other two articles discussing the formats used by calipers were also very helpful in getting my head around what was actually going on under the little plastic casings. [Harbor Frieght Caliper Digital Format](https://www.yuriystoys.com/2013/07/chinese-caliper-data-format.html) does a good job diving into a very similar format to BIN6 and links as well to [Chinese Scales](http://www.shumatech.com/support/chinese_scales.htm)

> Written with [StackEdit](https://stackedit.io/).