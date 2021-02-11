# AGPLv3 License

!!! attention

    **By using Nyx, you acknowledge that you have read and understood the open-source AGPLv3 license, as described [here](https://choosealicense.com/licenses/agpl-3.0/) and in the LICENSE file of Nyx.**

    Christopher Rabotin is the copyright holder of the source code of Nyx. The respective authors of programs which use Nyx are _not_ required to release the source code of their program _unless_ they convey a program which uses modified version of Nyx.

The AGPLv3 license is a <span class="emph">business-friendly</span> license which protects your intellectual property and your research. It encourages users to modify the source code of Nyx and distribute their changes to the broader community. Anyone is allowed to use Nyx in any way they please, a personal or commercial setting, and sell software which packages or uses an unmodified version of Nyx (_propagate_). Private and commercial entities may run a _modified_ version of Nyx without limitations as long as they do not _convey_ the modified version of Nyx to third parties whose usage they do not fully control.

!!! info

    To _propagate_ a work means to do anything with it that, without permission, would make you directly or secondarily liable for infringement under applicable copyright law, except executing it on a computer or modifying a private copy. Propagation includes copying, distribution (with or without modification), making available to the public, and in some countries other activities as well.

    To _convey_ a work means any kind of propagation that enables other parties to make or receive copies.  Mere interaction with a user through a computer network, with no transfer of a copy, is not conveying.

!!! help
    If you would like to discuss the terms of the license, please contact me at christopher [dot] rabotin [at] gmail [dot] com so I can put you in contact with a lawyer knowledgeable on open-source licenses.

## FAQ

The AGPLv3 license is often negatively portrayed in industry, so let's go through a few standard questions. In the following, the term _unmodified version_ corresponds to the officially released and sanctioned version of Nyx linked to from this website, nyxspace.com.

**TL;DR:** The license encourages you to build and sell programs on top of an unmodified version of Nyx, especially when those programs add a lot of value. Keep in mind that almost no customer can solely maintain a program which adds a lot of value without your help, so a custom is quite unlikely to become a competitor even if they have access to the source code. Also, you should really read the FAQ and contact a lawyer if you're super worried about free software even though the quasi-totality of webservers run Linux, which is free software.

### Can I sell results of analyzes without disclosing my code?
**Yes**, even if you use a modified version of Nyx, the output of Nyx or programs which use Nyx is _not_ subjected to the AGPLv3 license.

??? Example
    I wrote a program which uses a custom version of Nyx to run large scale Monte Carlo analyzes from my laptop. The project was funded by an external company and I will be providing the results of this work (but not the source code to generate the results) to that company. I _do not_ need to release the source code to anyone.

### Can I modify Nyx and keep those modifications to myself?
**Yes**, unless you allow other parties to make or receive a copy of that modified version, or of a program which requires that modified version.

### Can I sell access to a program which provides analysis results?
**Yes**, and you can keep the source to yourself unless you use a modified version of Nyx.

??? Example
    I wrote a super cool cloud-based Flight Dynamics System allowing external parties to plot the status of their constellations and run collision avoidance scenarios. All of the backend work uses an _unmodified_ version of Nyx, but the customers are not directly interacting with Nyx and only receive data products from Nyx. I _do not_ have to release the source code of that application.

### Can I sell programs which use an unmodified version of Nyx?
**Yes**, you may create and distribute (for free or for a fee) any program which runs on top of Nyx.

However, the AGPLv3 is a transitive ("viral") license, so you must release your plugin as AGPLv3 as well. This does not mean that you need to redistribute the code of your plugin at the time of distribution of your program, it only means that you must provide the source of your plugins at a _reasonable cost_ upon request by whomever has access to that plugin.

### Overall, am I required to release the code developed in a private/academic/industry setting?
**No**, unless you run a modified version of Nyx and are distributing your program to third parties whose use of your program is _not_ under your supervision.

??? Example
    1. I wrote a program which uses a **modified** version of Nyx to run large scale Monte Carlo analyzes from my company cloud deployment. The program will be used only within the company. I _do not_ need to make the source code available to anyone because this is considered _private use_, and is therefore unrestricted.
    2. I wrote a program which uses an **unmodified** version of Nyx to run large scale Monte Carlo analyzes from my company cloud deployment. The program will be available for use by external parties. I _do not_ need to make the source code available to anyone because I am using an **unmodified** version of Nyx.
    3. I wrote a program which uses an **modified** version of Nyx to run large scale Monte Carlo analyzes from my company cloud deployment. The program will be available for use by external parties. _Because_ I am running a **modified** version, upon request by these parties, and for a reasonable cost (or free and publicly if said parties is the general public), I _must_ make the source code of all programs and scripts required to execute the larger program available.

### Results from Nyx caused my customer to crash on the Moon!
Oops, that's too bad, please file a bug report. Nyx is provided without warranty of any kind.

!!! info
    As per the LICENSE file which was provided to you with the program, and that you've accepted by using Nyx:

    THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

### External contributions
Additions and modifications of Nyx are encouraged! They help the astrodynamics industry as a whole. The best place to start is by forking the code, modifying it, and opening a pull/merge request. As per the license agreement, if you hold a patent to the code you add or modify, you thereby grant permission to the users of Nyx to use said patent.

--8<-- "includes/Abbreviations.md"