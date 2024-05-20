/* eslint-disable react/jsx-key */
import { Button } from "frames.js/next"

export const images = [
  "https://i.imgur.com/bM67J6s.png",
  "https://i.imgur.com/igoXsBp.png",
  "https://i.imgur.com/eIHv5wk.png",
  "https://i.imgur.com/FAeFAga.png",
]

export default function getFramesContent(page: number, summary?: object): any {
  switch (page) {
    case 0:
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

    case 1: {
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

    case 2:
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

    case 3:
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
                op: "get_summary",
              },
            }}
          >
            Refresh
          </Button>,
        ],
      }

    case 4:
      return {
        image: (
          <div tw="flex flex-col bg-[#FFF9C4]">
            <div tw="flex">Your summary</div>

            <div tw="flex flex-col items-center justify-center">
              {Object.entries(summary!).map(([key, value]) => (
                <div tw="flex flex-col items-center justify-center">
                  <div tw="flex center">{key}:</div>
                  <div tw="flex center">{value}</div>
                </div>
              ))}
            </div>
          </div>
        ),
        buttons: [],
      }

    default: {
      return {
        image: <div tw="flex">Oops, how did we end up here?</div>,
        imageOptions: {
          aspectRatio: "1:1",
        },
        buttons: [],
      }
    }
  }
}
