export interface CollaborationGroup {
  group_id: number;
  name: string;
  description?: string;
  created_by: number;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  creator_name?: string;
  member_count?: number;
  member_role?: string;
}

export interface GroupMember {
  member_id: number;
  group_id: number;
  student_id: number;
  role: 'member' | 'admin';
  joined_at: string;
  name?: string;
  email?: string;
  department?: string;
}

export interface Discussion {
  discussion_id: number;
  group_id: number;
  title: string;
  created_by: number;
  created_at: string;
  is_pinned: boolean;
  creator_name?: string;
  message_count?: number;
}

export interface Message {
  message_id: number;
  discussion_id: number;
  author_id: number;
  content: string;
  created_at: string;
  updated_at: string;
  is_edited: boolean;
  author_name?: string;
}

export interface CreateGroupRequest {
  name: string;
  description?: string;
}

export interface CreateDiscussionRequest {
  title: string;
  group_id: number;
}

export interface CreateMessageRequest {
  content: string;
  discussion_id: number;
}

export interface JoinGroupRequest {
  student_id: number;
  role?: 'member' | 'admin';
}