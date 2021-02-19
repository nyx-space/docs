# AGPLv3 License

!!! attention

    **By using Nyx, you acknowledge that you have read and understood the free software AGPLv3 license, as described [here](https://choosealicense.com/licenses/agpl-3.0/) and in the LICENSE file of Nyx.**

    Christopher Rabotin is the copyright holder of the source code of Nyx. The respective authors of programs which use Nyx own the copyright to their own programs. The concept of "free software" uses the term "free" as in "free speech," not as in "free snacks."

## Executive summary
In the following, the term _unmodified version_ corresponds to the officially released and sanctioned version of Nyx linked to from this website, nyxspace.com.

1. The AGPLv3 license is a <span class="emph">business-friendly</span> license which protects your intellectual property and your research.
2. You, as a personal or commercial entity, are allowed to <span class="emph">sell data products</span> created from programs that require a _modified_ or _unmodified_ version of Nyx without limitations.
3. The license authorizes you to execute a _modified_ version of Nyx without limitation, as long as you do not distribute the software which executes the modified version of Nyx (_convey_).
4. If you distribute software which packages a _modified_ or _unmodified_ version of Nyx to third parties such that they may execute or distribute your software without your supervision or guidance, then your software must be distributed under the AGPLv3 license (_propagate_). In that case, if your program uses an _unmodified_ version of Nyx, the source code of your software must be made available to those third parties who have access to your software on their explicit request at a reasonable cost. If, however, you _propagate_ your software which uses a _modified_ version of Nyx, then the source code of your software must be made available to public, because Nyx itself is available to the public without limitation.
5. The AGPLv3 license encourages you to keep your intellectual property and only distribute/sell the data products from your program which uses Nyx. It also encourages you to share the changes you make to Nyx with the community of users of Nyx.
6. If you do not abide by the terms and conditions of this license, Christopher Rabotin reserves the right to terminate your license, revoke your access to Nyx, and file a lawsuit for copyright infringement.

!!! tip
    Keep in mind that almost no customer can maintain a value-adding program without your help, so a customer is quite unlikely to become a competitor even if they have access to the source code. Also remember that the world runs on free software: the quasi-totality of servers run GNU/Linux.

!!! info

    To _propagate_ a work means to do anything with it that, without permission, would make you directly or secondarily liable for infringement under applicable copyright law, except executing it on a computer or modifying a private copy. Propagation includes copying, distribution (with or without modification), making available to the public, and in some countries other activities as well.

    To _convey_ a work means any kind of propagation that enables other parties to make or receive copies.  Mere interaction with a user through a computer network, with no transfer of a copy, is not conveying.

!!! help
    If you would like to discuss the terms of the license, please contact me at christopher [dot] rabotin [at] gmail [dot] com so I can put you in contact with a lawyer knowledgeable on open-source licenses.

## FAQ

The AGPLv3 license is often unfairly and negatively portrayed in industry, so let's go through a few standard questions.

### Can I sell results of analyses without disclosing my code?
**Yes**, even if you use a modified version of Nyx, the output of Nyx or programs which use Nyx is _not_ subjected to the AGPLv3 license.

??? Example
    I wrote a program which uses a custom version of Nyx to run large scale Monte Carlo analyses from my laptop. The project was funded by an external company and I will be providing the results of this work (but not the source code to generate the results) to that company. I _do not_ need to release the source code to anyone.

### Can I modify Nyx and keep those modifications to myself?
**Yes**, unless you allow other parties to make or receive a copy of that modified version, or of a program which requires that modified version.

### Can I sell access to a program which provides analysis results?
**Yes**, and you do not need to publicly release the source if you use an _unmodified_ version of Nyx.

??? Example
    I wrote a super cool cloud-based Flight Dynamics System allowing external parties to plot the status of their constellations and run collision avoidance scenarios. All of the backend work uses an _unmodified_ version of Nyx, but the customers are not directly interacting with Nyx and only receive data products from Nyx. I _do not_ have to release the source code of that application.

### Can I sell programs which use an unmodified version of Nyx?
**Yes**, you may create and distribute (for free or for a fee) any program which runs on top of Nyx.

However, the AGPLv3 is a transitive ("viral") license, so you must release your program as AGPLv3 as well. This does not mean that you need to redistribute the code of your program at the time of distribution, it only means that you must provide the source of your program at a _reasonable cost_ upon request by whomever has access to that plugin.

### Overall, am I required to release the code developed in a private/academic/industry setting?
**No**, unless you run a modified version of Nyx and are distributing your program to third parties whose use of your program is _not_ under your supervision.

??? Example
    1. I wrote a program which uses a **modified** version of Nyx to run large scale Monte Carlo analyses from my company cloud deployment. The program will be used only within the company. I _do not_ need to make the source code available to anyone because this is considered _private use_, and is therefore unrestricted.
    2. I wrote a program which uses an **unmodified** version of Nyx to run large scale Monte Carlo analyses from my company cloud deployment. The program will be available for use by external parties. I _do not_ need to make the source code available to anyone because I am using an **unmodified** version of Nyx.
    3. I wrote a program which uses an **modified** version of Nyx to run large scale Monte Carlo analyses from my company cloud deployment. The program will be available for use by external parties. _Because_ I am running a **modified** version, upon request by these parties, and for a reasonable cost (or free and publicly if said parties is the general public), I _must_ make the source code of all programs and scripts required to execute the larger program available.

### Results from Nyx caused my customer to crash on the Moon!
Oops, that's too bad, please file a bug report. Nyx is provided without warranty of any kind.

!!! info
    As per the LICENSE file which was provided to you with the program, and that you've accepted by using Nyx:

    THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

### External contributions
Additions and modifications of Nyx are encouraged! They help the astrodynamics industry as a whole. The best place to start is by forking the code, modifying it, and opening a pull/merge request. As per the license agreement, if you hold a patent to the code you add or modify, you thereby grant permission to the users of Nyx to use said patent.

### See also
+ [GPLv3 official FAQ](https://www.gnu.org/licenses/gpl-faq.html)
+ [Violations of the GNU Licenses](https://www.gnu.org/licenses/gpl-violation.html)
+ [AGPLv3 source distribution](https://opensource.stackexchange.com/questions/5003/agplv3-source-redistribution-when-does-it-apply-to-my-code-for-a-server-side-ja)
+ [Express grant of patent rights?](https://opensource.stackexchange.com/questions/6302/what-does-express-grant-of-patent-rights-from-contributors-to-users-mean)

--8<-- "includes/Abbreviations.md"