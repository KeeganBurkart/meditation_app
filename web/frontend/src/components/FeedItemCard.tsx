import { useState } from "react";
import {
  addFeedComment,
  addFeedEncouragement,
  FeedComment,
  FeedEncouragement,
} from "../services/api";

export interface FeedItem {
  item_id: number;
  user_id: number;
  user_display_name?: string;
  item_type: string;
  message: string;
  comments?: FeedComment[];
  encouragements?: FeedEncouragement[];
}

interface Props {
  item: FeedItem;
}

export default function FeedItemCard({ item }: Props) {
  const [comments, setComments] = useState<FeedComment[]>(item.comments || []);
  const [encs, setEncs] = useState<FeedEncouragement[]>(item.encouragements || []);
  const [commentText, setCommentText] = useState("");
  const [encText, setEncText] = useState("");

  async function handleAddComment() {
    if (!commentText) return;
    const newComment = await addFeedComment(item.item_id, commentText);
    if (newComment) setComments([...comments, newComment]);
    setCommentText("");
  }

  async function handleAddEnc() {
    if (!encText) return;
    const newEnc = await addFeedEncouragement(item.item_id, encText);
    if (newEnc) setEncs([...encs, newEnc]);
    setEncText("");
  }

  return (
    <li>
      <p>
        <strong>{item.user_display_name || `User ${item.user_id}`}</strong>:{' '}
        {item.message}
      </p>
      {comments.length > 0 && (
        <ul>
          {comments.map((c) => (
            <li key={c.comment_id}>{c.text}</li>
          ))}
        </ul>
      )}
      {encs.length > 0 && (
        <ul>
          {encs.map((e) => (
            <li key={e.encouragement_id}>{e.text}</li>
          ))}
        </ul>
      )}
      <div>
        <input
          placeholder="Add comment"
          value={commentText}
          onChange={(e) => setCommentText(e.target.value)}
        />
        <button onClick={handleAddComment}>Comment</button>
      </div>
      <div>
        <input
          placeholder="Add encouragement"
          value={encText}
          onChange={(e) => setEncText(e.target.value)}
        />
        <button onClick={handleAddEnc}>Encourage</button>
      </div>
    </li>
  );
}
