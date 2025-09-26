import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  CollaborationGroup,
  GroupMember,
  Discussion,
  Message,
  CreateGroupRequest,
  CreateDiscussionRequest,
  CreateMessageRequest,
  JoinGroupRequest
} from '../models/collaboration';

@Injectable({
  providedIn: 'root'
})
export class CollaborationService {
  private apiUrl = 'http://localhost:8000/collaboration';

  constructor(private http: HttpClient) {}

  // Group management
  createGroup(group: CreateGroupRequest, createdBy: number): Observable<any> {
    const params = new HttpParams().set('created_by', createdBy.toString());
    return this.http.post<any>(`${this.apiUrl}/groups`, group, { params });
  }

  getGroups(studentId?: number): Observable<{ groups: CollaborationGroup[] }> {
    let params = new HttpParams();
    if (studentId) {
      params = params.set('student_id', studentId.toString());
    }
    return this.http.get<{ groups: CollaborationGroup[] }>(`${this.apiUrl}/groups`, { params });
  }

  joinGroup(groupId: number, member: JoinGroupRequest): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/groups/${groupId}/members`, member);
  }

  getGroupMembers(groupId: number): Observable<{ members: GroupMember[] }> {
    return this.http.get<{ members: GroupMember[] }>(`${this.apiUrl}/groups/${groupId}/members`);
  }

  // Discussion management
  createDiscussion(discussion: CreateDiscussionRequest, createdBy: number): Observable<any> {
    const params = new HttpParams().set('created_by', createdBy.toString());
    return this.http.post<any>(`${this.apiUrl}/groups/${discussion.group_id}/discussions`, discussion, { params });
  }

  getGroupDiscussions(groupId: number): Observable<{ discussions: Discussion[] }> {
    return this.http.get<{ discussions: Discussion[] }>(`${this.apiUrl}/groups/${groupId}/discussions`);
  }

  // Message management
  createMessage(message: CreateMessageRequest, authorId: number): Observable<any> {
    const params = new HttpParams().set('author_id', authorId.toString());
    return this.http.post<any>(`${this.apiUrl}/discussions/${message.discussion_id}/messages`, message, { params });
  }

  getDiscussionMessages(discussionId: number, studentId: number): Observable<{ messages: Message[] }> {
    const params = new HttpParams().set('student_id', studentId.toString());
    return this.http.get<{ messages: Message[] }>(`${this.apiUrl}/discussions/${discussionId}/messages`, { params });
  }
}