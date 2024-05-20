/* eslint-disable react/jsx-key */
import { Button } from "frames.js/next"
import { frames } from "./frames"
import { appURL } from "../utils"

const images = [
  "https://i.imgur.com/bM67J6s.png",
  "https://i.imgur.com/igoXsBp.png",
  "https://i.imgur.com/eIHv5wk.png",
]

const frameHandler = frames(async (ctx: any) => {
  const page = Number(ctx.searchParams?.pageIndex ?? 0)
  const op = ctx.searchParams?.op
  const inputText = ctx.message?.inputText
  const requesterFid = ctx.message?.requesterFid

  if (page === 0) {
    return {
      image: images[page]!,
      imageOptions: {
        aspectRatio: "1:1",
      },
      buttons: [
        <Button
          action="post"
          target={{
            query: {
              pageIndex: String(page + 1),
            },
          }}
        >
          Start
        </Button>,
      ],
    }
  }

  if (page === 1) {
    console.log(`fetch here feed of fid ${requesterFid}`)

    return {
      image: images[page]!,
      imageOptions: {
        aspectRatio: "1:1",
      },
      textInput: "Type in your interest here...",
      buttons: [
        <Button
          action="post"
          target={{
            pathname: "/",
            query: {
              pageIndex: String(page + 1), // % nfts.length),
              op: "choose_interest_for_me",
            },
          }}
        >
          Choose for me!
        </Button>,
        <Button
          action="post"
          target={{
            pathname: "/",
            query: {
              pageIndex: String(page + 1),
              op: "typed_interest",
            },
          }}
        >
          Typed my interest!
        </Button>,
      ],
    }
  }

  if (page === 2) {
    console.log(
      `let the agents run on ${
        op === "choose_interest_for_me"
          ? "chooese for me"
          : `typed my interest ${ctx.message?.inputText}`
      }`
    )

    return {
      image: images[page]!,
      imageOptions: {
        aspectRatio: "1:1",
      },
      buttons: [
        <Button
          action="post"
          target={{
            pathname: "/",
            query: {
              pageIndex: String(page + 1),
              op: "serve_castlatte",
            },
          }}
        >
          Serve my Castlatte
        </Button>,
      ],
    }
  }

  if (page === 3) {
    console.log("check if agents have finished, if not show page 2 again")

    return {
      image: (
        <div tw="flex flex-col">
          <div tw="flex">Your summary</div>

          <div tw="flex">AI generated summary</div>
        </div>
      ),
      buttons: [],
    }
  }

  return {
    image: <div tw="flex">Oops, how did we end up here?</div>,
  }
})

export const GET = frameHandler
export const POST = frameHandler
