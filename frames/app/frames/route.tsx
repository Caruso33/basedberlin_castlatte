/* eslint-disable react/jsx-key */
import { Button } from "frames.js/next"
import { frames } from "./frames"
import { appURL } from "../utils"
import getFramesContent from "./content"

const frameHandler = frames(async (ctx: any) => {
  const page = Number(ctx.searchParams?.pageIndex ?? 0)
  const op = ctx.searchParams?.op
  const inputText = ctx.message?.inputText
  const requesterFid = ctx.message?.requesterFid

  if (page === 0) {
    return getFramesContent(page)
  }

  if (page === 1) {
    console.log(`fetch here feed of fid ${requesterFid}`)

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_FARCASTER_BACKEND_URL}/feed/${requesterFid}`
    )
    const data = await response.json()
    console.log(`page 1 response casts length ${data.length}`)

    return getFramesContent(page)
  }

  if (page === 2) {
    console.log(
      `let the agents run on ${
        op === "choose_interest_for_me"
          ? "chooese for me"
          : `typed my interest ${inputText}`
      }`
    )

    const interests =
      op === "choose_interest_for_me" ? "Ethereum price sentiment" : inputText

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_FARCASTER_BACKEND_URL}/process_feed/${requesterFid}?interests=${interests}`
    )
    const data = await response.json()
    console.log(`page 2 response result ${data}`)

    return getFramesContent(page)
  }

  if (page === 3) {
    console.log("show castlatte info")

    return getFramesContent(page)
  }

  if (page === 4) {
    console.log("check if agents have finished, if not show page 3 again")

    console.log("requesterId", requesterFid)

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_FARCASTER_BACKEND_URL}/summary/${requesterFid}`
    )

    if (!response.ok) {
      return getFramesContent(3)
    }

    const data = await response.json()
    console.log(`page 4 response casts length ${data}`)

    return getFramesContent(page, data)
  }

  return getFramesContent(page)
})

export const GET = frameHandler
export const POST = frameHandler
