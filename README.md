# md0: Simple Markdown Subset for Painless Parsing

md0 is a format for hypertext documents. It is designed to be extremely easy to parse and is a proper subset of markdown. The main goal is to make it easier to share text-based content online, for authors, readers, and tool builders. The original motivation is to create a format that can be easily consumed by resource-constrained devices.

md0 consists of two simple extensions to plain text: links and images, as follows:

- a *link ref* takes the form `[word][n]` where `word` is a sequence of characters, none of which is a space, an opening bracket `[`, or a closing bracket `]`, and `n` is a positive integer (non-zero). There must be a space between a link ref and any preceeding text; if there is text immediately after a link ref (without a space), the text should be rendered as plain text. This is to support cases like `check out this [link][2]!`
- a *link def* takes the form `[n]: link` where `n` is a positive integer and `link` is a sequence of non-space characters. Each link def must go on its own line, and all link refs must come after the main text content.
- an *image ref* takes the form `![alt text][n]` where `alt text` is a sequence of characters, none of which is an opening bracket `[`, or a closing bracket `]`, and `n` is a positive integer. Link defs for images take the same form as above.

All other text is treated as plain text. This document is a valid md0 file despite the use of *bold* and `code` syntax from markdown - those will simply be rendered verbatim. 

Text is rendered line-by-line, and each line is rendered word-by-word (words are delimited by spaces), so consequtive spaces will be treated as a single space (but consequtive lines will be preserved). A link ref should be rendered in a way to distinguish it from plain text. This includes rendering it as-is (`[word][n]` already indicates its is a link), as `word` with an underline, in a different font, with a different background color, etc.

The following is a self-contained Python program that renders md0 with a monospace font that can be used as a reference implementation, together with an example input and output.
