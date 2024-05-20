/* eslint-disable react/jsx-key */
import { Button } from "frames.js/next"
import { frames } from "./frames"
import { appURL } from "../utils"
import getFramesContent, { images } from "./content"

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

    return getFramesContent(page)
  }

  if (page === 3) {
    console.log("check if agents have finished, if not show page 2 again")

    return getFramesContent(page)
  }

  return getFramesContent(page)
})

export const GET = frameHandler
export const POST = frameHandler
