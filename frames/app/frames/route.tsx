/* eslint-disable react/jsx-key */
import { Button } from "frames.js/next"
import { frames } from "./frames"
import { appURL } from "../utils"

const frameHandler = frames(async (ctx: any) => {
  const page = Number(ctx.searchParams?.pageIndex ?? 0)

  const counter = ctx.message
    ? ctx.searchParams.op === "+"
      ? ctx.state.counter + 1
      : ctx.state.counter - 1
    : ctx.state.counter

  if (page === 0) {
    return {
      image: (
        <div tw="flex flex-col">
          <div tw="flex">Milk your Feed</div>

          <div tw="flex">Cream your Interest</div>

          {/* {ctx.message?.inputText && (
          <div tw="flex">{`Input: ${ctx.message.inputText}`}</div>
        )} */}
          {/* <div tw="flex">Test {counter}</div> */}
        </div>
      ),
      // textInput: "Say something",
      buttons: [
        <Button
          action="post"
          // target={{ pathname: "/", query: { op: "+" } }}
          target={{
            query: {
              pageIndex: String(page + 1), // % nfts.length),
            },
          }}
        >
          Start
        </Button>,
        // <Button action="post" target={{ pathname: "/", query: { op: "-" } }}>
        //   Decrement
        // </Button>,
        // <Button action="link" target={appURL()}>
        //   External
        // </Button>,
      ],
      state: { counter: counter },
    }
  }

  if (page === 1) {
    return {
      image: (
        <div tw="flex flex-col">
          <div tw="flex">
            Type in your interests to customize your 24h feed digest
          </div>

          <div tw="flex">or let us choose for you!</div>

          {ctx.message?.inputText && (
            <div tw="flex">{`Input: ${ctx.message.inputText}`}</div>
          )}
        </div>
      ),
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
        // <Button action="link" target={appURL()}>
        //   External
        // </Button>,
      ],
      state: { counter: counter },
    }
  }

  if (page === 2) {
    return {
      image: (
        <div tw="flex flex-col">
          <div tw="flex">
            AI Agents crew is tuning into your interests and brewing your
            Castlatte!
          </div>

          <div tw="flex">Tryi in 2 minutes!</div>
        </div>
      ),
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
      state: { counter: counter },
    }
  }
})

export const GET = frameHandler
export const POST = frameHandler
