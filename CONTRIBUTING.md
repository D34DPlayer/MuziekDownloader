# Contributing

[![Merged PRs][prs-merged-image]][prs-merged-url]
[![GitHub contributors][contributors-image]][contributors-url]
[![license][license-image]][license-url]

[prs-merged-url]: https://github.com/D34DPlayer/MuziekDownloader/pulls?q=is:pr+is:merged
[prs-merged-image]: https://img.shields.io/github/issues-pr-closed-raw/d34dplayer/muziekdownloader?color=green&label=merged%20PRs&style=flat-square
[contributors-url]: https://github.com/D34DPlayer/MuziekDownloader/graphs/contributors
[contributors-image]: https://img.shields.io/github/contributors/d34dplayer/muziekdownloader?color=blue&style=flat-square
[license-url]: https://github.com/D34DPlayer/MuziekDownloader/blob/main/LICENSE
[license-image]: https://img.shields.io/github/license/d34dplayer/muziekdownloader?style=flat-square

Contributions to the MuziekDownloader project are welcome!
Just open an issue or send a pull request and we'll incorporate it as soon as possible.

*Note*: when submitting a new feature, don't forget to check if there's already a pull request in progress for it.

## Submitting a pull request

Every pull request should handle a single "functionality" and be direcited to the [dev branch](https://github.com/D34DPlayer/MuziekDownloader/tree/dev). 
Don't be afraid to make multiple PRs if you want to add multiple functionalities.

### Commit message

For the commit message, use the following format:
```
   ACTION: [AUDIENCE:] COMMIT_MSG [!TAG ...]

 Description

   ACTION is one of 'chg', 'fix', 'new'

       Is WHAT the change is about.

       'chg' is for refactor, small improvement, cosmetic changes...
       
       'fix' is for bug fixes
       
       'new' is for new features, big improvement

   AUDIENCE is optional and one of 'dev', 'usr', 'pkg', 'test', 'doc'

       Is WHO is concerned by the change.

       'dev'  is for developpers (API changes, refactors...)
       'usr'  is for final users (UI changes)
       'pkg'  is for packagers   (packaging changes)
       'test' is for testers     (test only related changes)
       'doc'  is for doc guys    (doc only changes)

   COMMIT_MSG is ... well ... the commit message itself.

   TAGs are additionnal adjective as 'refactor' 'minor' 'cosmetic'

       They are preceded with a '!' or a '@' (prefer the former, as the
       latter is wrongly interpreted in github.) Commonly used tags are:

       'refactor' is obviously for refactoring code only
       
      'minor' is for a very meaningless change (a typo, adding a comment)
      
       'cosmetic' is for cosmetic driven change (re-indentation, 80-col...)
       
       'wip' is for partial functionality but complete subfunctionality.

 Examples:

   new: usr: support of bazaar implemented
   chg: re-indentend some lines !cosmetic
   new: dev: updated code to be compatible with last version of killer lib.
   fix: pkg: updated year of licence coverage.
   new: test: added a bunch of test around user usability of feature X.
   fix: typo in spelling my name in comment. !minor
```

## Licensing

This repository is licensed under the [MIT license](LICENSE).
